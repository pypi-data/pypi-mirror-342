# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2014-2017 Canonical Ltd.
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
from __future__ import unicode_literals

import io
import logging
import os
import sys


import byov
from byoc import (
    registries,
    stacks,
)
from byot import fixtures
from byov import (
    config,
)
from byov.tests import features

try:
    if sys.version_info < (3,):
        # novaclient doesn't support python3 (yet)
        from byov.vms import nova
except ImportError:
    pass
try:
    from byov.vms import ec2
    with_boto3 = bool(ec2)  # silly trick to pacify pyflakes
except ImportError:
    # No boto3, no ec2 vms.
    with_boto3 = False


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


# Useful shortcuts
patch = fixtures.patch
override_env = fixtures.override_env


def isolate_from_disk(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup as well as an /etc/ one so tests can setup
    config files.
    """
    fixtures.set_uniq_cwd(test)
    fixtures.isolate_from_env(test)
    # Isolate tests from the user environment
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    # byov.path is supposed to default to invocation directory, for tests this
    # is uniq_dir
    fixtures.patch(test, byov, 'path', [test.uniq_dir])
    fixtures.override_env(test, 'BYOV_PATH', ':'.join(byov.path))
    os.mkdir(test.home_dir)
    fixtures.override_env(test, 'HOME', test.home_dir)
    # Also isolate from the system environment
    test.etc_dir = os.path.join(test.uniq_dir, config.system_config_dir()[1:])
    os.makedirs(test.etc_dir)
    fixtures.patch(test, config, 'system_config_dir', lambda: test.etc_dir)

    # Make sure config stores don't leak via the shared stores
    # byoc.stacks._shared_stores. vm.run_hook has to save all known config
    # stores before running to make sure any hook modification is properly
    # seen.
    fixtures.patch(test, stacks, '_shared_stores', {})


def set_uniq_vm_name(test, short=False):
    """To isolate tests from each other, created vms need a unique name.

    To keep those names legal and still user-readable we use the class name and
    the test method name. The process id is added so that the same test suite
    can be run on the same host in several processes.

    :param short: Defaults to False. Use only the test method and the pid. This
        helps with qemu unix socket names being limited in length.
    """
    meth = test._testMethodName
    pid = os.getpid()
    if short:
        vm_name = '{meth}-{pid}'.format(**locals())
    else:
        cname = test.__class__.__name__
        vm_name = '{cname}-{meth}-{pid}'.format(**locals())
    # '_' are not valid in hostnames
    test.vm_name = vm_name.replace('_', '-')


class _MyStreamHandler(logging.StreamHandler):
    """Work around an issue in python2 urllib3 library not using unicode.

    Can be deleted once we migrate to python3 novaclient.
    """

    def emit(self, record):
        msg = record.msg
        if sys.version_info < (3,) and isinstance(msg, str):
            record.msg = msg.decode('utf8')
        super(_MyStreamHandler, self).emit(record)


def override_logging(test, debug=None):
    """Setup a logging handler, restoring the actual handlers after the test.

    This assumes a logging setup where handlers are added to the root logger
    only.

    :param debug: When set to True, log output with level debug is sent to
        stdout.
    """
    # FIXME: Should we ask for '{logging.level}' instead ? -- vila 2022-01-07
    env_debug = bool(os.environ.get('DEBUG', False))
    if debug is None and env_debug:
        debug = env_debug
    if debug:
        stream = sys.stdout
        level = logging.DEBUG
    else:
        stream = io.StringIO()
        level = logging.INFO
    root_logger = logging.getLogger(None)
    # Using reversed() below ensures we can modify root_logger.handlers as well
    # as providing the handlers in the right order for cleanups.
    for handler in reversed(root_logger.handlers):
        root_logger.removeHandler(handler)
        test.addCleanup(root_logger.addHandler, handler)
    # Install the new handler
    test.log_stream = stream
    new_handler = _MyStreamHandler(stream)
    test.addCleanup(root_logger.removeHandler, new_handler)
    root_logger.addHandler(new_handler)
    # Install the new level, restoring the actual one after the test
    test.addCleanup(root_logger.setLevel, root_logger.level)
    root_logger.setLevel(level)


# Registries for various test setups

class Setup:
    # The following should be set by the daughter classes
    vm_class = None
    required_features = []

    def setup_conf(self, test, conf):
        """Setup the configuration for a test."""
        # FIXME: This forces some tests to specify more than they really need
        # (at least release and arch should be easier to deal with). As in this
        # setup impose too much constraints to tests to be the default. A
        # 'test' backend may be worth exploring.  -- vila 2024-09-22

        # For a given test, some options are shared for all vms
        no_name = config.VmStack(None)
        conf.set('vm.name', test.vm_name)
        no_name.set('vm.class', test.kls)
        no_name.set('vm.distribution', test.dist)
        no_name.set('vm.release', test.series)
        no_name.set('vm.architecture', test.arch)
        return conf

    def setup_vm(self, test, conf):
        """Setup a vm for a given configuration.

        :param test: The test that will use the vm.

        :return: The built vm.
        """
        return conf.get('vm.class')(conf)

    def before_isolation(self, test, user_conf):
        """Acquire data from `user_conf` to be used as test resources.

        :param test: The test before it's isolated (i.e. can access user env).

        :param user_conf: The user configuration providing test resources.
        """
        pass

    def after_isolation(self, test, conf):
        """Early setup for the isolated test.

        :param test: The already isolated  test.

        :param conf: The test configuration providing test resources.
        """
        pass

    def isolate(self, test):
        """Setup user provided configuration for tests.

        The isolation from env and disk is in the middle of this method. Two
        entry points are provided: before_isolation and after_isolation the
        former can collect whatever is needed in the user environment so the
        later can access dedicated user resources.

        A self.uniq_dir/etc/byov.conf is created from
        ~/.config/byov/byov.conf-tests with a pre-defined set of config
        options.

        If files ending with '.conf-tests' exist under '~/.config/byov/conf.d',
        they are installed under 'test.etc_dir/conf.d' without the '-tests'
        suffix.
        """
        # Get a user configuration before isolation
        user_conf = config.VmStack(None)

        # Stop here if there is no user provided test configs
        features.test_requires(test, features.tests_config)
        self.before_isolation(test, user_conf)

        # the following calls isolate_from_env and create unique dirs
        isolate_from_disk(test)
        # From now on, the user env cannot be accessed and the test owns its
        # env.

        # Make user provided test config files visible to tests by installing
        # them under self.uniq_dir/etc/byov/conf.d
        def install(src, dst):
            with open(src) as s, open(dst, 'w') as d:
                d.write(s.read())
        install(features.tests_config.user_path,
                os.path.join(test.etc_dir, config.config_file_basename()))
        if features.tests_config.more_paths:
            confd_dir = os.path.join(test.etc_dir, 'conf.d')
            os.mkdir(confd_dir)
            for p in features.tests_config.more_paths:
                _, bname = os.path.split(p)
                # Drop the -tests suffix from the basename
                # FIXME: This trick should probably be refactored by installing
                # (where ?) a hook to read directly from those files and stop
                # creating copies and squatting the file namespace
                # -- vila 2022-04-04
                install(p, os.path.join(confd_dir, bname[:-len('-tests')]))

        # Create a config file for tests (all set() go to the section chosen at
        # Stack creation time)
        conf = config.VmStack(test.vm_name)
        # FIXME: parametrized by distro and arch in a way that can be
        # controlled from the command line ? -- vila 2024-07-04

        # Unless tests themselves override it, vm.release depends on the
        # distribution. While for regular users the vm.release should have no
        # default value, for tests, the need exist to not specify what release
        # has to be tested but delegate to distribution which sees.

        # FIXME: There needs to be a way to define which distribution,
        # architecture and releases need to be tested. It's unclear that a
        # single test run should cover all combinations though
        # -- vila 2024-07-04

        # FIXME: Forcing stable below was a bad idea and the wrong way to
        # control which release is tested by default. Keep the code commented
        # out as a reminder until a better implementation is available
        # -- vila 2024-12-14
        # conf.set('vm.release', '{{vm.distribution}.release.stable}')

        # Some tests assumes -oLogLevel=ERROR is part of ssh.options to avoid
        # the 'Warning: Permanently added xxx to the list of known hosts.'
        test.assertTrue('-oLogLevel=ERROR' in conf.get('ssh.options'))

        # If there is no ssh key or its pub counterpart is not in
        # authorized_keys, we won't be able to connect to vms
        key_path = conf.get('ssh.key')
        test.assertTrue(os.path.exists(key_path),
                        '{} does not exist'.format(key_path))
        authorized_keys = conf.get('ssh.authorized_keys')
        test.assertTrue(key_path + '.pub' in authorized_keys)

        # Give early access to the test object with a config already populated
        self.after_isolation(test, conf)

        # Persist changes to disk
        conf.store.save()

        # Reboot the config stacks building from disks
        config.import_user_byovs()
        # The conf is ready to use
        return conf


test_setups = registries.Registry()


def register_setup(setup):
    test_setups.register(setup.vm_class, setup, setup.__doc__)


class DockerSetup(Setup):
    """Setup a docker vm for tests."""

    vm_class = 'docker'
    required_features = [features.docker_client_feature]

    def setup_conf(self, test, conf):
        conf = super().setup_conf(test, conf)
        # To trigger the image cleanup
        conf.set('docker.image.unpublish.command',
                 'docker, image, rm, -f,' + test.vm_name.lower())
        image = conf.get('docker.image')
        with io.open('./Dockerfile', 'w', encoding='utf8') as f:
            f.write('''\
FROM {}
# FIXME: This is a mistake, building the image should not require running the
# container as ENTRYPOINT can interfer with it. -- vila 2022-03-01
# Force the container to stay up once started
ENTRYPOINT ["sleep", "infinity"]
'''.format(image))
        return conf


register_setup(DockerSetup)


class Ec2Setup(Setup):
    """Setup an ec2 server for tests."""

    vm_class = 'ec2'
    required_features = [features.ec2_creds, features.ec2_boto3]

    def after_isolation(self, test, conf):
        super().after_isolation(test, conf)
        # ec2 test resources get some specific tags
        conf.set('ec2.instance.tags', 'test.id ' + test.id())
        conf.set('ec2.image.tags', 'test.id ' + test.id())

    def setup_conf(self, test, conf):
        conf = super().setup_conf(test, conf)
        # Set to the empty string to use 'ec2.distribution.images'
        conf.set('ec2.image', '')
        conf.set('vm.published_as', '{vm.name}-public')
        if test.dist == "amazon":
            # at least on al2, dnf is not installed
            conf.set('dnf.command', 'sudo, yum, {dnf.options}')
            conf.set('dnf.options', '-y, -t')
        return conf


register_setup(Ec2Setup)


class LxdSetup(Setup):
    """Setup an lxd container for tests."""

    vm_class = 'lxd'
    required_features = [features.lxd_client_feature]

    def before_isolation(self, test, user_conf):
        super().before_isolation(test, user_conf)
        # FIXME: This is the default value, but it should probably also check
        # LXD_CONF so, best to make it an option -- vila 2024--09-24
        test.lxd_conf_dir = os.path.expanduser('~/.config/lxc')

    def after_isolation(self, test, conf):
        super().after_isolation(test, conf)
        fixtures.override_env(test, 'LXD_CONF', test.lxd_conf_dir)

    def setup_conf(self, test, conf):
        conf = super().setup_conf(test, conf)
        conf.set('vm.published_as', '{vm.name}-public')
        return conf

register_setup(LxdSetup)


class NovaSetup(Setup):
    """Setup a nova server for tests."""

    vm_class = 'nova'
    required_features = [features.nova_creds]

    def setup_conf(self, test, conf):
        conf = super().setup_conf(test, conf)
        image_id = nova.byov_image_name('cloudimg', test.series, test.arch)
        conf.set('nova.image', image_id)
        return conf

register_setup(NovaSetup)


class QemuSetup(Setup):
    """Setup a qemu vm for tests."""

    vm_class = 'qemu'
    required_features = [features.qemu_img_feature]

    def before_isolation(self, test, user_conf):
        # qemu relies on images being provided (hence downloaded) by the user,
        # tests just reuse them.
        test.user_download_dir = user_conf.get('qemu.download.dir')

    def setup_conf(self, test, conf):
        conf = super().setup_conf(test, conf)
        features.requires_existing_bridge(test, conf.get('qemu.bridge'))
        features.requires_usable_bridge(test, conf)
        conf.set('qemu.networks',
                 '-net bridge,br={qemu.bridge}'
                 ' -net nic,macaddr={qemu.mac.address}')
        # Unless the test overrides it, qemu vms reuse downloads provided by
        # the user but use a private image dir.
        conf.set('qemu.download.dir', test.user_download_dir)
        test.images_dir = os.path.join(test.uniq_dir, 'images')
        conf.set('qemu.images.dir', test.images_dir)
        # Unless the test says otherwise (and/or publish the image), provides
        # some sane (uniq) default
        conf.set('vm.published_as', '{qemu.image}-public')
        # FIXME: qemu.image.setup and qemu.image.teardown ?
        # -- vila 2019-12-07
        return conf

register_setup(QemuSetup)


class ScalewaySetup(Setup):
    """Setup a scaleway server for tests."""

    vm_class = 'scaleway'
    required_features = [features.scaleway_creds]

    def setup_conf(self, test, conf):
        conf = super().setup_conf(test, conf)
        conf.set('scaleway.flavor', 'START1-XS')
        conf.set('scaleway.image',
                 '{vm.distribution}/{vm.release}/{vm.architecture}-xs')
        # conf.set('scaleway.flavor', 'C1')
        # conf.set('vm.architecture', 'armhf')
        features.test_requires(test, features.ScalewayImage(conf))
        return conf


register_setup(ScalewaySetup)


def setup_conf(test):
    """Setup the config environment for the given test.

    This requires the test to provide a `kls` attribute which is used to get
    the backend specific Setup object.

    After this function is called, the test is isolated from environment and
    disk.  This allows tests (as well as backends) to peak into the user
    provided resources before isolating the test.
    """
    setup = test_setups.get(test.kls)()
    if setup.required_features:
        # Check features
        for f in setup.required_features:
            if not f.available():
                test.skipTest('{} is not available'.format(f.feature_name()))
    conf = setup.isolate(test)
    if getattr(test, 'setup_conf', None):
        conf = test.setup_conf(conf)
    # Some setup classes require additional and specific config
    conf = setup.setup_conf(test, conf)
    if getattr(test, 'setup_conf', None) is not None:
        # The test itself has the last word
        conf = test.setup_conf(conf)
    backend_setup = getattr(test, 'setup_conf_' + test.kls, None)
    if backend_setup is not None:
        # The test itself has the last word for backend specifics
        conf = backend_setup(conf)
    # save all config changes
    conf.store.save()
    return conf


def setup_vm(test, conf=None):
    """Setup a vm for the given test.

    This allows backend to create test-specific vms based on `kls`. The test
    itself can define a `setup_vm` method to further refine the vm.
    """
    if conf is None:
        conf = test.conf
    setup = test_setups.get(test.kls)()
    vm = setup.setup_vm(test, conf)
    if getattr(test, 'setup_vm', None) is not None:
        # The test itself has the last word
        vm = test.setup_vm(conf, vm)
    backend_setup = getattr(test, 'setup_vm_' + test.kls, None)
    if backend_setup is not None:
        # The test itself has the last word for backend specifics
        vm = backend_setup(conf, vm)
    return vm
