# This file is part of Build Your Own Virtual machine.
#
# Copyright 2019 Vincent Ladeuil.
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
import os
import unittest


from urllib import parse

from byov import (
    config,
    errors,
)
from byov.tests import (
    features,
    fixtures,
)


@features.requires(features.wget_feature)
class TestDownloadImage(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        # Downloading real isos or images is too long for tests, instead, we
        # fake it by downloading a small but known to exist file.
        super().setUp()
        self.vm_name = 'foo'
        self.conf = fixtures.setup_conf(self)
        download_dir = os.path.join(self.uniq_dir, 'downloads')
        os.mkdir(download_dir)
        fixtures.override_logging(self)
        conf = self.conf
        orig_url = conf.get('qemu.download.url')
        # FIXME: Possibly via a test specific config option we could define the
        # name of the small file as distribution specific -- vila 2024-12-11
        self.download_url = parse.urljoin(orig_url, 'SHA512SUMS')
        conf.set('qemu.download.dir', download_dir)
        conf.set('qemu.download.url', self.download_url)
        conf.set('qemu.image.setup', 'download')
        conf.set('qemu.image.teardown', 'download')
        conf.set('qemu.image', '{qemu.download.path}')
        self.vm = fixtures.setup_vm(self)

    def test_download_succeeds(self):
        vm = self.vm
        vm.setup_image()
        self.assertTrue(os.path.exists(vm.disk_image_path()))
        # Trying to download again will find the file in the cache
        self.assertFalse('Already at' in self.log_stream.getvalue())
        vm.setup_image()
        self.assertTrue('Already at' in self.log_stream.getvalue())

    def test_download_creates_cache(self):
        download_dir = os.path.join(self.uniq_dir, 'I-dont-exist')
        self.conf.set('qemu.download.dir', download_dir)
        vm = self.vm
        self.assertFalse(os.path.exists(os.path.dirname(vm.disk_image_path())))
        vm.setup_image()
        self.assertTrue(os.path.exists(vm.disk_image_path()))

    def test_download_unknown_fails(self):
        # Sabotage the valid url
        url = self.conf.get('qemu.download.url')
        self.conf.set('qemu.download.url', url + 'I-dont-exist')
        vm = self.vm
        self.assertRaises(errors.CommandError, vm.setup_image)


@features.requires(features.qemu_img_feature)
class TestConvertImage(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        self.vm_name = 'foo'
        self.conf = fixtures.setup_conf(self)
        features.requires_existing_path(self, self.user_download_dir)
        convert_dir = os.path.join(self.uniq_dir, 'convert')
        conf = self.conf
        conf.set('vm.disk_size', '2.5G')  # Limit the size for tests
        conf.set('qemu.download.dir', self.user_download_dir)
        conf.set('qemu.images.dir', convert_dir)
        conf.set('qemu.image.setup', 'convert,resize')
        conf.set('qemu.image.teardown', 'convert')
        features.requires_existing_path(self, conf.get('qemu.download.path'))
        self.vm = fixtures.setup_vm(self)

    def test_convert_image(self):
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        self.vm.setup_image()
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))

    def test_convert_no_source(self):
        self.conf.set('qemu.download.path', 'I-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('I-dont-exist' in cm.exception.err)

    def test_convert_too_small(self):
        # This is a lower bound to the reference image which is unlikely to
        # shrink below that.
        self.conf.set('vm.disk_size', '200M')
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('Use the --shrink' in cm.exception.err)
        # The resize failed but the image exists (if only to help set the
        # proper size)
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))


@features.requires(features.qemu_img_feature)
class TestClone(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        self.vm_name = 'foo'
        self.conf = fixtures.setup_conf(self)
        features.requires_existing_path(self, self.user_download_dir)
        conf = self.conf
        features.requires_existing_path(self, conf.get('qemu.download.path'))

        # Setup the shared config
        conf = config.VmStack(None)
        conf.set('vm.disk_size', '2.5G')  # Limit the size for tests
        conf.set('qemu.download.dir', self.user_download_dir)

        clone_dir = os.path.join(self.uniq_dir, 'clone')
        conf.set('qemu.images.dir', clone_dir)
        conf.set('qemu.image.setup', 'clone,resize')
        conf.set('qemu.image.teardown', 'clone')
        # Points to the reference image
        self.bconf = config.VmStack('base')
        self.bconf.set('vm.published_as', '{qemu.download.path}')
        self.conf.set('vm.backing', 'base')

        # Save self.conf, conf, and bconf
        conf.store.save()
        self.vm = fixtures.setup_vm(self)

    def test_clone_image(self):
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        self.vm.setup_image()
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))

    def test_clone_no_source(self):
        self.bconf.set('vm.published_as', 'I-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('I-dont-exist' in cm.exception.err)

    def test_clone_too_small(self):
        # This is a lower bound to the reference image which is unlikely to
        # shrink below that.
        self.conf.set('vm.disk_size', '200M')
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('Use the --shrink' in cm.exception.err)
        # The resize failed but the image exists (if only to help set the
        # proper size)
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))


@features.requires(features.qemu_img_feature)
@features.requires(features.ovmf)
class TestUEFIVars(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        self.vm_name = 'foo'
        self.conf = fixtures.setup_conf(self)
        features.requires_existing_path(self, self.user_download_dir)
        clone_dir = os.path.join(self.uniq_dir, 'clone')

        conf = self.conf
        conf.set('qemu.download.dir', self.user_download_dir)
        conf.set('qemu.images.dir', clone_dir)
        conf.set('qemu.image.setup', 'uefi.vars')
        conf.set('qemu.image.teardown', 'uefi.vars')
        conf.store.save()
        self.vm = fixtures.setup_vm(self, conf)

    def test_vars_are_created(self):
        vars_path = self.vm.conf.get('qemu.uefi.vars.path')
        self.assertFalse(os.path.exists(vars_path))
        self.vm.setup_image()
        self.assertTrue(os.path.exists(vars_path))

    def test_no_seed(self):
        self.conf.set('qemu.uefi.vars.seed', '/I-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('/I-dont-exist' in cm.exception.err)

    def test_qemu_disks(self):
        qemu_disks = ' '.join(self.vm.conf.get('qemu.disks.uefi'))
        vars_path = self.vm.conf.get('qemu.uefi.vars.path')
        code_path = self.vm.conf.get('qemu.uefi.code.path')
        self.assertIn(vars_path, qemu_disks)
        self.assertIn(code_path, qemu_disks)


@features.requires(features.geniso_feature)
@features.requires(features.qemu_img_feature)
class TestSeedImage(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        self.vm_name = 'foo'
        self.conf = fixtures.setup_conf(self)
        features.requires_existing_path(self, self.user_download_dir)
        images_dir = os.path.join(self.uniq_dir, 'images')
        self.conf.set('qemu.images.dir', images_dir)
        self.vm = fixtures.setup_vm(self)

    def test_create_seed_image(self):
        self.assertTrue(self.vm._seed_path is None)
        self.vm.create_seed_image()
        self.assertFalse(self.vm._seed_path is None)
        self.assertTrue(os.path.exists(self.vm._seed_path))


@features.requires(features.qemu_feature)
class TestQemuMonitor(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self)
        self.conf = fixtures.setup_conf(self)
        conf = self.conf
        features.requires_existing_path(self, self.user_download_dir)
        features.requires_existing_path(self, conf.get('qemu.download.path'))
        self.vm = fixtures.setup_vm(self)

    def test_terminate_qemu(self):
        # smoke test but it requires a properly setup vm (spawn_qemu can't be
        # called without some pre-requisites and makes it hard to debug this
        # test otherwise)
        vm = self.vm
        vm.setup()
        self.addCleanup(vm.terminate_qemu)
        self.assertEqual('RUNNING', vm.state())


@features.requires(features.geniso_feature)
class TestSetupWithSeed(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self, short=True)
        self.conf = fixtures.setup_conf(self)
        conf = self.conf
        features.requires_existing_path(self, self.user_download_dir)
        features.requires_existing_path(self, conf.get('qemu.download.path'))
        fixtures.override_logging(self)
        features.requires_existing_bridge(self, conf.get('qemu.bridge'))
        features.requires_usable_bridge(self, conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        conf.set('vm.update', 'False')  # Shorten install time
        conf.set('vm.cpus', '2')
        conf.set('vm.disk_size', '2.5G')  # Limit the size for tests
        conf.set('qemu.download.dir', self.user_download_dir)
        conf.set('qemu.images.dir', images_dir)
        conf.set('qemu.image.setup', 'download,convert,resize')
        conf.set('qemu.image.teardown', 'convert,resize')
        conf.set('vm.name', self.vm_name)
        conf.set('qemu.networks',
                 '-net bridge,br={qemu.bridge}'
                 ' -net nic,macaddr={qemu.mac.address}')
        self.vm = fixtures.setup_vm(self)

    def test_setup_with_seed(self):
        self.addCleanup(self.vm.teardown, force=True)
        self.vm.setup()
        self.assertEqual('RUNNING', self.vm.state())

    def test_start_keeps_mac(self):
        self.addCleanup(self.vm.teardown, force=True)
        self.vm.setup()
        self.assertEqual('RUNNING', self.vm.state())
        mac_address = self.vm.econf.get('qemu.mac.address')
        ip_address = self.vm.econf.get('vm.ip')
        self.vm.stop()
        self.vm.start()
        self.assertEqual(mac_address, self.vm.econf.get('qemu.mac.address'))
        # The aim is to get a stable ip so it must be the same on all starts
        self.assertEqual(ip_address, self.vm.econf.get('vm.ip'))


@features.requires(features.geniso_feature)
class TestSetupWithBacking(unittest.TestCase):

    kls = 'qemu'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self, short=True)
        self.conf = fixtures.setup_conf(self)
        conf = self.conf
        features.requires_existing_path(self, self.user_download_dir)
        features.requires_existing_path(self, conf.get('qemu.download.path'))
        fixtures.override_logging(self)
        features.requires_existing_bridge(self, conf.get('qemu.bridge'))
        features.requires_usable_bridge(self, conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        conf.set('vm.update', 'False')  # Shorten install time
        conf.set('vm.disk_size', '2.5G')  # Limit the size for tests

        conf.set('qemu.download.dir', self.user_download_dir)
        conf.set('qemu.images.dir', images_dir)
        conf.set('qemu.image.setup', 'clone,resize')
        conf.set('qemu.image.teardown', 'clone')
        conf.set('qemu.networks',
                 '-net bridge,br={qemu.bridge}'
                 ' -net nic,macaddr={qemu.mac.address}')
        conf.store.save()

        bconf = config.VmStack('base')
        bconf.set('vm.name', 'base')

        vconf = self.conf
        vconf.set('vm.name', self.vm_name)
        vconf.set('vm.backing', 'base')

        # Points to the reference image
        bconf.set('qemu.download.dir', self.user_download_dir)
        bconf.set('vm.published_as', '{qemu.download.path}')

        # conf, bconf and vconf are all in the same store, a single save is
        # enough
        self.assertTrue(conf.store == vconf.store)
        self.assertTrue(conf.store == bconf.store)
        conf.store.save()
        self.vm = fixtures.setup_vm(self)

    def test_setup_with_backing(self):
        vm = self.vm
        self.addCleanup(vm.teardown, force=True)
        vm.setup()
        self.assertEqual('RUNNING', vm.state())

# FIXME: While vm.update=False makes the test faster, it missed the bug where
# Qemu.setup() wasn't waiting for cloud-init to finish leading to a very
# confusing behavior. Specifically, cloud-init add-apt-repository (for a ppa)
# raced with the first apt-get update issued by byov.
# -- vila 2019-12-03
