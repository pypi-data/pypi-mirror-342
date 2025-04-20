# This file is part of Build Your Own Virtual machine.
#
# Copyright 2022 Vincent Ladeuil.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""The docker backend is significantly different from other ones as it doesn't
rely on cloud-init at all because most features are already supported in docker
files.

Similarly, because docker provides an easy shell access, ssh is not needed nor
used.

Instead, we rely on docker files expanding them from the byov provided
configuration files.

"""
# FIXME: https://github.com/moby/buildkit/issues/1186 clearly shows where
# docker is heading: towards docker devs comfort, against users one. Since even
# stdout/stderr roles are subject to chage, all bets are off. It may be that
# switching the command-line based implementation to one integrated with
# https://docker-py.readthedocs.io/en/stable/index.html could be more robust ?
# -- vila 2025-04-12
import json
import logging
import os
import pty
import tempfile
import time


from byov import (
    errors,
    subprocesses,
    vms,
)


logger = logging.getLogger(__name__)


def container_info(vm_name):
    info = dict(state='UNKNOWN')
    cmd = ['docker', 'container', 'inspect', vm_name]
    ret, out, err = subprocesses.run(cmd, raise_on_error=False)
    jout = json.loads(out)
    if jout:
        # We asked for a single container inspection
        jout = jout[0]
        # Extract only the info we need
        # Finally, translate the state
        # https://stackoverflow.com/questions/32427684/
        # what-are-the-possible-states-for-a-docker-container#32428199
        docker_states = dict(created='STOPPED',
                             restarting='RUNNING',
                             running='RUNNING',
                             paused='STOPPED',
                             exited='STOPPED',
                             dead='UNKNOWN')
        info['state'] = docker_states[jout['State']['Status']]
        pass
    return info


class Docker(vms.VM):
    """docker container."""

    vm_class = 'docker'
    setup_ip_timeouts = 'docker.setup_ip.timeouts'
    existing_vm_options = vms.VM.existing_vm_options + [
        'docker.image.id', 'docker.container.id']

    def state(self):
        # man lxc(7) defines the possible states as: STOPPED, STARTING,
        # RUNNING, ABORTING, STOPPING. We add UNKNOWN.
        info = container_info(self.conf.get('vm.name'))
        return info['state']

    def run_create_image_hook(self):
        """Locally run a setup command defined by the user."""
        return self.run_hook('docker.create.image.hook')

    def create_image(self):
        logger.info('Creating docker image for {}...'.format(
            self.conf.get('vm.name')))
        self.run_create_image_hook()
        orig_dir = os.getcwd()
        try:
            dbase = self.conf.get('docker.base')
            os.chdir(dbase)
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf8',
                                             dir=os.getcwd()) as f:
                content = self.expand_file(self.conf.get('docker.file'))
                f.write(content)
                f.flush()
                self.conf.set('docker.file.expanded', f.name)
                create_command = self.conf.get('docker.image.build.command')
                # lower vm name so it can be used for image tag or docker
                # complains
                tag = self.conf.get('vm.name').lower()
                create_command += ['--tag={}'.format(tag)]
                # Force --quiet to get the image id on stdout.
                create_command += ['--quiet']
                create_command += ['--file', f.name, dbase]
                ret, out, err = subprocesses.run(create_command)
                img_id = out[0:-1].split(':')[1]
                self.econf.set('docker.image.id', img_id)
                self.save_existing_config()
        finally:
            os.chdir(orig_dir)

    def create(self):
        logger.info('Creating {} docker container...'.format(
            self.conf.get('vm.name')))
        orig_dir = os.getcwd()
        try:
            os.chdir(self.conf.get('docker.base'))
            create_command = self.conf.get('docker.container.create.command')
            create_command += ['--name', self.conf.get('vm.name')]
            mounts = self.conf.get('docker.mounts')
            if mounts:
                create_command.extend(mounts)
            ports = self.conf.get('docker.ports')
            if ports:
                create_command.extend(['-p=' + p for p in ports])

            create_command.append(self.conf.get('docker.image.id'))
            ret, out, err = subprocesses.run(create_command)
            self.save_existing_config()
        finally:
            os.chdir(orig_dir)

    def start(self):
        super().start()
        logger.info('Starting {} docker container...'.format(
            self.conf.get('vm.name')))
        start_command = self.conf.get('docker.container.start.command')
        ret, out, err = subprocesses.run(start_command)
        self.save_existing_config()

    def upload(self, local_path, remote_path, mode_bits=None):
        logger.info('Copying {} into {} docker container...'.format(
            local_path, self.conf.get('vm.name')))
        if mode_bits is None:
            # Keep only the last 3 digits as that's what chmod will
            # accept. This will raises if path doesn't exist
            mode_bits = oct(self._mode_bits(local_path))[-3:]
        cp_command = self.conf.get('docker.container.cp.command')
        cp_command += [local_path]
        cp_command += ['{}:{}'.format(self.conf.get('vm.name'), remote_path)]
        ret, out, err = subprocesses.run(cp_command)
        chmod_command = self.conf.get('docker.container.shell.command')
        chmod_command += [self.conf.get('vm.name'),
                          'chmod', mode_bits, remote_path]
        ret, out, err = subprocesses.run(chmod_command)

    def shell(self, command, *args):
        if command and command.startswith('@'):
            retcode, out, err = self.run_script(
                command[1:], args=args, captured=False)
        else:
            # docker fails to properly connect if it doesn't get a pty
            cmd = self.conf.get('docker.container.shell.command')
            if not command:
                cmd += ['-t']
            cmd += [self.conf.get('vm.name')]
            if not command:
                cmd += [self.conf.get('vm.user.shell')]
            else:
                cmd += [command] + list(args)
            retcode = pty.spawn(cmd)
            out, err = None, None  # nope, can't get that easily from pty
            if retcode:
                raise errors.CommandError(cmd, retcode, out, err)
        return retcode, out, err

    def get_ssh_command(self, command, *args):
        """Just a root shell access."""
        cmd = self.conf.get('docker.container.shell.command')
        cmd += [self.conf.get('vm.name')]
        if command is not None:
            # There is no sudo by default (and it's not needed, we *are* root)
            if command != 'sudo':
                cmd += [command]
            if args:
                cmd += args
        return cmd

    def wait_for_setup(self):
        logger.info('Waiting for container {} to be ready...'.format(
            self.conf.get('vm.name')))
        # FIXME: Why is this relevant ? I.e. when can it fail ?  Isn't it more
        # significant to rely on update commands to all succeed ? Meanwhile, it
        # could should catch really bad errors but never fail when setup
        # succeed...  -- vila 2023-12-20
        check = self.conf.get('docker.setup.done')
        logger.info('Using {} to check.'.format(check))
        stos = self.conf.get('docker.setup.timeouts')
        me = self.wait_for_setup.__name__
        for attempt, sleep in enumerate(stos):
            try:
                if attempt > 1:
                    logger.debug('Re-trying {} {}/{}'.format(
                        me, attempt, stos.retries))
                ret, out, err = self.shell(*check)
                return
            except Exception:
                logger.debug(
                    '{} is not ready yet'.format(
                        self.conf.get('vm.name')),
                    exc_info=True)
            # FIXME: metric  -- vila 2022-05-03
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, stos.retries))
            time.sleep(sleep)
        raise errors.ByovError('{name} setup ({check}) never succeeded',
                               name=self.conf.get('vm.name'), check=check)

    def setup(self):
        # https://stackoverflow.com/questions/37744961/docker-run-vs-create
        logger.info('Setting up {} docker container...'.format(
            self.conf.get('vm.name')))
        self.create_image()
        self.create()
        self.start()
        self.setup_over_ssh()
        self.wait_for_setup()

    def stop(self, now=False):
        logger.info('Stopping {} docker container...'.format(
            self.conf.get('vm.name')))
        orig = None
        if now:
            orig = self.conf.get('docker.container.stop.timeout',
                                 convert=False)
            self.conf.set('docker.container.stop.timeout', '0')
        try:
            stop_command = self.conf.get('docker.container.stop.command')
            ret, out, err = subprocesses.run(stop_command)
        finally:
            if orig is not None:
                self.conf.set('docker.container.stop.timeout', orig)

    def publish(self):
        img_name = self.conf.get('vm.published_as')
        logger.info('Publishing {} docker image from {}...'.format(
            img_name, self.conf.get('vm.name')))
        tag_command = self.conf.get('docker.image.tag.command')
        ret, out, err = subprocesses.run(tag_command)
        publish_command = self.conf.get('docker.image.publish.command')
        ret, out, err = subprocesses.run(publish_command)

    def unpublish(self):
        unpublish_command = self.conf.get('docker.image.unpublish.command')
        logger.info('Un-publishing with {}...'.format(unpublish_command))
        ret, out, err = subprocesses.run(unpublish_command)

    def teardown(self, force=False):
        logger.info('Tearing down {} docker container...'.format(
            self.conf.get('vm.name')))
        if force and self.state() == 'RUNNING':
            self.stop(now=True)
        teardown_command = self.conf.get('docker.container.teardown.command')
        ret, out, err = subprocesses.run(teardown_command)
        # FIXME: delete the image too ? -- vila 2022-01-14
        super().teardown()
