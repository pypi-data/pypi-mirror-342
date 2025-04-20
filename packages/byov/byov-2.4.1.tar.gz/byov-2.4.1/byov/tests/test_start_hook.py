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

import os
import unittest

from byov import errors
from byov.tests import (
    features,
    fixtures,
)


class TestStartHook(unittest.TestCase):

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
        fixtures.override_logging(self)
        conf = self.conf
        conf.set('vm.class', 'ephemeral-lxd')
        conf.set('vm.backing', self.base_vm)
        self.vm = fixtures.setup_vm(self)

    def test_empty_hook(self):
        self.conf.set('vm.start.hook', '')
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_failing_hook(self):
        self.conf.set('vm.start.hook', 'i-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.start()
        self.assertEqual(127, cm.exception.retcode)
        self.assertEqual('/bin/sh: 1: i-dont-exist: not found\n',
                         cm.exception.err)

    def test_hook_success(self):
        self.conf.set('vm.start.hook', 'touch me')
        self.addCleanup(self.vm.stop)
        self.vm.start()
        self.assertTrue(os.path.exists('me'))

    def test_hook_script_success(self):
        self.conf.set('content', 'touch me')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh\n{content}\n''')
        os.chmod('script', 0o755)
        self.conf.set('vm.start.hook', '@script')
        self.addCleanup(self.vm.stop)
        self.vm.start()
        self.assertTrue(os.path.exists('me'))

    def test_hook_script_fails(self):
        self.conf.set('content', 'false')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh\n{content}\n''')
        os.chmod('script', 0o755)
        self.conf.set('vm.start.hook', '@script')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.start()
        self.assertEqual(1, cm.exception.retcode)


class TestStartHookConfig(unittest.TestCase):

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
        self.vm = fixtures.setup_vm(self)
        fixtures.override_logging(self)

    def test_hook_flush_configs(self):
        with open('byov.conf', 'w') as f:
            f.write('''sentinel = now you see me\n''')
        self.assertEqual('now you see me', self.conf.get('sentinel'))
        with open('script', 'w') as f:
            f.write('''#!/bin/sh
echo "sentinel = now you dont" > byov.conf
''')
        os.chmod('script', 0o755)
        self.conf.set('vm.start.hook', '@script')
        self.addCleanup(self.vm.stop)
        self.vm.start()
        self.assertEqual('now you dont', self.conf.get('sentinel'))
