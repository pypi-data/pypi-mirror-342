# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
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

import errno
import os
import unittest


import byov


from byov import errors
from byov.tests import (
    features,
    fixtures,
)


class TestPush(unittest.TestCase):

    kls = 'lxd'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self)
        self.conf = fixtures.setup_conf(self)
        self.base_vm = 'byov-tests-lxd-debian'
        features.requires_existing_vm(self, self.base_vm)
        conf = self.conf
        conf.set('vm.class', 'ephemeral-lxd')
        conf.set('vm.backing', self.base_vm)
        conf.set('test.dir', self.uniq_dir)
        features.requires_existing_vm(self, 'byov-tests-lxd-debian')
        self.vm = fixtures.setup_vm(self)
        self.addCleanup(self.vm.stop)
        self.vm.start()

    def test_simple(self):
        local = 'foo'
        with open(local, 'w') as f:
            f.write('quux')
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        ret = self.vm.push(local, remote)
        self.assertEqual(0, ret)
        ret, _, _ = self.vm.shell_captured('test', '-f', remote)
        self.assertEqual(0, ret)

    def test_local_found_in_path(self):
        fixtures.patch(self, byov, 'path', [os.path.expanduser('~/'),
                                            self.uniq_dir])
        local = 'home/foo'
        # create a local file
        with open(local, 'w') as f:
            f.write('{vm.name}')
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        # push local to remote (expanding options in file name if needed)
        ret = self.vm.push('@foo', remote)
        self.assertEqual(0, ret)
        # get remote back
        ret, out, _ = self.vm.shell_captured('cat', remote)
        self.assertEqual(0, ret)
        # ensure roundtrip success: the file content has been expanded
        self.assertEqual(self.vm.conf.get('vm.name'), out)

    def test_expanded(self):
        local = 'foo'
        # create a local file
        with open(local, 'w') as f:
            f.write('{vm.name}')
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        # push local to remote (expanding options in file name if needed)
        ret = self.vm.push('@{test.dir}/' + local, remote)
        self.assertEqual(0, ret)
        # get remote back
        ret, out, _ = self.vm.shell_captured('cat', remote)
        self.assertEqual(0, ret)
        # ensure roundtrip success: the file content has been expanded
        self.assertEqual(self.vm.conf.get('vm.name'), out)

    def test_unknown_src(self):
        local = 'foo'
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        with self.assertRaises(OSError) as cm:
            self.vm.push(local, remote)
        self.assertEqual(errno.ENOENT, cm.exception.errno)
        self.assertEqual(local, cm.exception.filename)

    def test_unknown_dst(self):
        local = 'foo'
        with open(local, 'w') as f:
            f.write('quux')
        remote = '/bar'
        with self.assertRaises(errors.CommandError):
            self.vm.push(local, remote)
