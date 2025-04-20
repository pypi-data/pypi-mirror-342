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

import os
import unittest

from byov import errors
from byov.tests import (
    features as features,
    fixtures as fixtures,
)


class TestPull(unittest.TestCase):

    kls = 'lxd'
    dist = 'debian'
    series = 'trixie'
    arch = 'amd64'

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_vm_name(self)
        self.conf = fixtures.setup_conf(self)
        features.requires_existing_vm(self, 'byov-tests-lxd-debian')
        self.conf.set('vm.class', 'ephemeral-lxd')
        self.conf.set('vm.backing', 'byov-tests-lxd-debian')
        self.vm = fixtures.setup_vm(self)
        self.addCleanup(self.vm.stop)
        self.vm.start()

    def test_simple(self):
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        ret, _, _ = self.vm.shell_captured('echo', 'quux', '>' + remote)
        self.assertEqual(0, ret)
        local = 'foo'
        ret = self.vm.pull(remote, local)
        self.assertEqual(0, ret)
        ret, _, _ = self.vm.shell_captured('test', '-f', remote)
        self.assertEqual(0, ret)

    def test_unknown_src(self):
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        local = 'foo'
        with self.assertRaises(errors.CommandError):
            self.vm.pull(remote, local)

    def test_unknown_dst(self):
        remote = '/home/{}/bar'.format(self.vm.conf.get('vm.user'))
        ret, _, _ = self.vm.shell_captured('echo', 'quux', '>' + remote)
        self.assertEqual(0, ret)
        local = 'I-dont-exist/foo'
        self.assertFalse(os.path.exists(os.path.dirname(local)))
        self.vm.pull(remote, local)
        self.assertTrue(os.path.exists(os.path.dirname(local)))
