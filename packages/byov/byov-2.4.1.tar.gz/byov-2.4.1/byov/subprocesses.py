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
import errno
import logging
import os
import subprocess


from byov import errors


logger = logging.getLogger(__name__)


def run(args, cmd_input=None, raise_on_error=True):
    """Run the specified command capturing output and errors.

    :param args: A list of a command and its arguments.

    :param cmd_input: A unicode string to feed the command with.

    :param raise_on_error: A boolean controlling whether or not an exception is
        raised if the command fails.

    :return: A tuple of the return code, the output and the errors as unicode
        strings.

    """
    full_cmd = ' '.join(args)
    stdin = None
    if cmd_input is not None:
        stdin = subprocess.PIPE
        full_cmd += ' ' + cmd_input
        cmd_input = cmd_input.encode('utf8')
    logger.debug('Running {}'.format(full_cmd))
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=stdin)
    out, err = proc.communicate(cmd_input)
    out = out.decode('utf8')
    err = err.decode('utf8')
    if raise_on_error and proc.returncode:
        raise errors.CommandError([full_cmd], proc.returncode, out, err)
    logger.debug('Returned: {}'.format(proc.returncode))
    if out:
        logger.debug('stdout: {}'.format(out))
    if err:
        logger.debug('stderr: {}'.format(err))
    return proc.returncode, out, err


def raw_run(args):
    """Run the specified command without redirecting anything.

    This is mainly useful to wrap a command leaving std{in,out,err}
    untouched so the user can interact.

    :param args:  A list of a command and its arguments.

    :return: The return code.
    """
    logger.debug('Running {}'.format(' '.join(args)))
    proc = subprocess.Popen(args)
    proc.wait()
    return proc.returncode


def pipe(args):
    """Run the specified command as a pipe.

    The caller is responsible for processing the output and the errors.

    :param args:  A list of a command and its arguments.

    :return: The Popen object.
    """
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc


def which(command, path, mode=os.F_OK | os.X_OK):
    """Given a `command`, a `path` list of strings and a `mode`, return the
    first normalized file path which conforms to the given mode in the
    directories listed in `path`, or None if there is no such file.

    `mode` defaults to os.F_OK | os.X_OK.

    This is heavily inspired by `shutils.which` but the API is significantly
    different and the implementation simpler.

    An important difference is that `shutils.which` ignore PATH when queried
    with a relative path. Whereas here, relative paths are attempted in
    all directories of `path`.

    """
    # Shortest alternative to f-strings supporting older pythons (trusty)
    # Should be easy to find when dropping trusty support.
    def f(s, **kwargs):
        return s.format(**kwargs)

    # expanduser does nothing if the path does not start with '~' so it's safe
    # to call in all cases
    command = os.path.expanduser(command)
    if os.path.isabs(command):
        name = os.path.normpath(command)
        if os.path.exists(name):
            if os.access(name, mode):
                return name
            else:
                raise PermissionError(
                    errno.EACCES,
                    f('{name} does not match mode: {mode}', **locals()),
                    command)
    if path:
        seen = set()
        for d in path:
            normdir = os.path.normpath(d)
            if normdir not in seen:
                name = os.path.join(d, os.path.normpath(command))
                if os.path.exists(name):
                    if os.access(name, mode):
                        return name
                    else:
                        raise PermissionError(
                            errno.EACCES,
                            f('{name} does not match mode: {mode}',
                              **locals()),
                            command)
                # Don't search the same dir more than once. This matters only
                # if we keep searching as this function returns xor raise an
                # exception if nothing is found so the `seen` set is purely
                # local.
                seen.add(normdir)
    else:
        msg = f('{command} not found in: {path}', **locals())
        raise FileNotFoundError(
            errno.ENOENT, f('{command} not found in: {path}',
                            **locals()),
            command)
