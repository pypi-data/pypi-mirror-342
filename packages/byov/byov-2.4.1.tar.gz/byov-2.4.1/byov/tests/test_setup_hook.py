# This file is part of Build Your Own Virtual machine.
#
# Copyright 2017-2018 Vincent Ladeuil.
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

import errno
import io
import os
import unittest

from byov import errors
from byov.tests import (
    features,
    fixtures,
)


class TestSetupHook(unittest.TestCase):

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
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        conf = self.conf
        conf.set('vm.class', 'ephemeral-lxd')
        conf.set('vm.backing', self.base_vm)
        self.vm = fixtures.setup_vm(self)

    def test_empty_hook(self):
        self.conf.set('vm.setup.hook', '')
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_non_existing_hook(self):
        self.conf.set('vm.setup.hook', 'i-dont-exist')
        self.addCleanup(self.vm.stop)
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.start()
        self.assertEqual(127, cm.exception.retcode)
        self.assertEqual('/bin/sh: 1: i-dont-exist: not found\n',
                         cm.exception.err)

    def test_hook_success(self):
        self.conf.set('vm.setup.hook', 'ls -d .')
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_hook_script_success(self):
        self.conf.set('content', 'true')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh\n{content}\n''')
        os.chmod('script', 0o755)
        self.conf.set('vm.setup.hook', '@script')
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_expanded_hook_script_success(self):
        self.conf.set('content', 'true')
        self.conf.set('script.path', 'script')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh\n{content}\n''')
        os.chmod('script', 0o755)
        self.conf.set('vm.setup.hook', '@{script.path}')
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_hook_expanded_command_success(self):
        self.conf.set('test.command', 'echo {vm.name}')
        self.conf.set('test.setup.hook', '{test.command}')
        ret, out, err = self.vm.run_hook('test.setup.hook')
        self.assertEqual(0, ret)
        self.assertEqual(self.vm_name, out.rstrip())

    def test_hook_script_fails(self):
        self.conf.set('content', 'false')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh -e\n{content}\ntrue\n''')
        os.chmod('script', 0o755)
        self.conf.set('vm.setup.hook', '@script')
        self.addCleanup(self.vm.stop)
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.start()
        self.assertEqual(1, cm.exception.retcode)

    def test_hook_non_executable_script_fails(self):
        self.conf.set('content', 'false')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh -e\n{content}\ntrue\n''')
        self.conf.set('vm.setup.hook', '@script')
        self.addCleanup(self.vm.stop)
        with self.assertRaises(PermissionError) as cm:
            self.vm.start()
        self.assertEqual(errno.EACCES, cm.exception.errno)
