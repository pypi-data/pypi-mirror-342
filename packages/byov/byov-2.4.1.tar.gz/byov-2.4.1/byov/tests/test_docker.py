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

import io
import unittest

from byoc import errors
from byov import (
    config,
)
from byov.tests import (
    features,
    fixtures,
)
from byov.vms import docker


@features.requires(features.docker_client_feature)
class TestContainerInspect(unittest.TestCase):

    kls = 'docker'
    dist = 'debian'  # unused
    series = 'unused'
    arch = 'unused'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self)
        self.conf = fixtures.setup_conf(self)

    def setup_vm(self, conf, vm):
        self.addCleanup(vm.teardown, True)
        return vm

    def setup_vm_docker(self, conf, vm):
        # image cleanup, tests needs to add the cleanup
        conf.set('docker.image.unpublish.command',
                 'docker, image, rm, -f,' + conf.vm_name.lower())
        # unpublish has to come after teardown (i.e. added for cleanup
        # before) when cleaning up or docker complains the image is still
        # referenced
        self.addCleanup(vm.unpublish)
        return vm

    def define_docker(self, definition):
        with io.open('./Dockerfile', 'w', encoding='utf8') as f:
            f.write(definition)
        vm = fixtures.setup_vm(self)
        vm.setup()
        self.addCleanup(vm.stop)
        return vm

    def test_unknown(self):
        info = docker.container_info('idontexist')
        self.assertEqual('UNKNOWN', info['state'])

    def test_running(self):
        vm = self.define_docker('''
FROM alpine
# Force the container to stay up once started
ENTRYPOINT ["sleep", "infinity"]
''')
        vm.start()
        self.assertEqual('RUNNING', vm.state())

    def test_stopped(self):
        vm = self.define_docker('''
FROM alpine
# Force the container to stay up once started
ENTRYPOINT ["sleep", "infinity"]
''')
        vm.stop()
        self.assertEqual('STOPPED', vm.state())


# FIXME: parametrized by distribution ? -- vila 2017-12-06
@features.requires(features.docker_client_feature)
class TestSetup(unittest.TestCase):

    kls = 'docker'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self)
        self.conf = fixtures.setup_conf(self)
        self.vm = fixtures.setup_vm(self)
        with io.open('./Dockerfile', 'w', encoding='utf8') as f:
            f.write('''
FROM {}
# Force the container to stay up once started
ENTRYPOINT ["sleep", "infinity"]
            '''.format(self.conf.get('docker.image')))

    def setup_vm(self, conf, vm):
        return vm

    def setup_vm_docker(self, conf, vm):
        features.test_requires(self, features.DockerRegistry())
        conf.set('vm.published_as', '{vm.name}-public')
        # image cleanup, tests needs to add the cleanup
        conf.set('docker.image.unpublish.command',
                 'docker, image, rm, -f,' + conf.vm_name.lower())
        # unpublish has to come after teardown (i.e. added for cleanup
        # before) when cleaning up or docker complains the image is still
        # referenced
        self.addCleanup(vm.unpublish)
        return vm

    def test_usable(self):
        vm = docker.Docker(config.VmStack(self.vm_name))
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        # We should be able to ssh with the right user
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)
        # Defaulting to root is bad, even if it's docker's fault
        self.assertEqual('root' + '\n', out)

    def test_update(self):
        fixtures.override_logging(self)
        vm = docker.Docker(config.VmStack(self.vm_name))
        vm.conf.set('vm.update', 'True')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        # We should be able to ssh with the right user
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)


class TestDockerMountsOption(unittest.TestCase):

    kls = 'docker'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'
    maxDiff = None

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self)
        self.conf = fixtures.setup_conf(self)

    def _test_invalid(self, val):
        self.conf.set('docker.mounts', val)
        with self.assertRaises(errors.OptionValueError) as cm:
            self.conf.get('docker.mounts')
        self.assertEqual(val, cm.exception.value)

    def test_invalid_type(self):
        self._test_invalid('wrong:~:/there')

    def test_invalid_readonly(self):
        self._test_invalid('bind:~:/home:read')

    def test_invalid_share(self):
        self._test_invalid('bind:~:/home:readonly:notashare')

    def test_bind_mount(self):
        self.conf.set('docker.mounts', 'bind:~:/home:readonly:rslave')
        self.assertEqual(
            ['--mount=type=bind,src={},dst=/home'
             ',readonly,bind-propagation=rslave'.format(
                 self.home_dir)],
            self.conf.get('docker.mounts'))

    def test_tmpfs_mount(self):
        self.conf.set('docker.mounts', 'tmpfs:/tmp:65536:1777')
        self.assertEqual(
            ['--mount=type=tmpfs,dst=/tmp,tmpfs-size=65536,tmpfs-mode=1777'],
            self.conf.get('docker.mounts'))

    def test_volume_mount(self):
        self.conf.set('docker.mounts', 'volume:volname:/there')
        self.assertEqual(
            ['--mount=type=volume,src=volname,dst=/there'],
            self.conf.get('docker.mounts'))
