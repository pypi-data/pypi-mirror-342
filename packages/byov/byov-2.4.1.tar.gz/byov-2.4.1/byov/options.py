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
import getpass
import logging
import os
import sys


import byov


from byoc import (
    options,
    registries,
)
from byov import (
    subprocesses,
    timeouts,
)

# Official API
Option = options.Option
ListOption = options.ListOption
PathOption = options.PathOption
RegistryOption = options.RegistryOption
MANDATORY = options.MANDATORY
OptionMandatoryValueError = options.errors.OptionMandatoryValueError
option_registry = options.option_registry
register = options.register


logger = logging.getLogger(__name__)


class PackageListOption(ListOption):
    """A package list option definition.

    This possibly expands '@filename' replacing it with the file content.
    """

    def __init__(self, *args, **kwargs):
        # Force invalid values to be an error (and forbids overriding it) to
        # catch invalid file names
        super().__init__(*args, invalid='error', **kwargs)

    def from_unicode(self, string):
        values = super().from_unicode(string)
        if not values:
            return values
        converted = []
        for v in values:
            if v.startswith('@'):
                packages_path = os.path.expanduser(v[1:])
                try:
                    # FIXME: A bit more care should be taken about interpreting
                    # relative paths: are they relative to the config file
                    # (they probably should ) ? Should subprocess.which()
                    # (hence byov.path) be used instead ?  Also, the current
                    # implementation swallow the ValueError raised below,
                    # turning it into an OptionValueError instead, losing the
                    # precision if multiple files are involved
                    # -- vila 2024-09-14
                    with open(packages_path) as f:
                        for package in f.read().splitlines():
                            comment = package.find('#')
                            if comment >= 0:
                                # Delete comments
                                package = package[0:comment]
                                package = package.rstrip()
                            if package == '':
                                # Ignore empty lines
                                continue
                            converted.append(package)
                except FileNotFoundError:
                    raise ValueError('{} does not exist'.format(v[1:]))
            else:
                converted.append(v)
        return converted


class LxdUserMountsOption(ListOption):
    """A list option definition for lxd user mounts.

    The list should contain pairs of host paths/vm paths.
    The host paths will be mounted at the vm paths with the user uid/gid.
    """

    def __init__(self, *args, **kwargs):
        # Force invalid values to be an error (and forbid overriding it) to
        # catch invalid file names
        super().__init__(
            *args, invalid='error', **kwargs)

    def from_unicode(self, string):
        values = super().from_unicode(string)
        if not values:
            return values
        converted = []
        for pair in values:
            try:
                host_path, vm_path = pair.split(':')
            except ValueError:
                raise ValueError('Invalid path pair in: {}'.format(pair))
            host_path = os.path.expanduser(host_path)
            if not os.path.isabs(host_path):
                # We're on thin ice if byovm is not run from the directory
                # where the byov.conf file is (which should also be the
                # invocation directory ?)...
                host_path = os.path.realpath(
                    os.path.join(os.getcwd(), host_path))
            if not os.path.isabs(vm_path):
                raise ValueError('{} must be absolute'.format(vm_path))
            converted.append((host_path, vm_path))
        return converted


class DockerMountsOption(ListOption):
    """A list option definition for docker mounts.

    This relies on VOLUMEs being defined in the docker image.
    The list should contain type-specific tuples.
    """
    def __init__(self, *args, **kwargs):
        # Foce invalid values to be an error (and forbids overriding it) to
        # catch invalid directories
        super().__init__(
            *args, invalid='error', **kwargs)

    def parse_bind(self, mnt):
        tmpl = '--mount=type=bind,src={src},dst={dst}'
        valid_shares = ('rprivate', 'private',
                        'rshared', 'shared',
                        'rslave', 'slave')
        values = mnt.split(':')
        src, dst = values[1:3]
        src = os.path.expanduser(src)
        if not os.path.isabs(src):
            # We're on thin ice if byovm is not run from the directory where
            # the byov.conf file is (which should also be the invocation
            # directory ?)...
            src = os.path.realpath(os.path.join(os.getcwd(), src))
        if not os.path.isabs(src):
            raise ValueError('{} must be absolute'.format(src))
        ro = False
        share = None
        if len(values) > 3:
            ro = values[3]
            if ro != 'readonly':
                raise ValueError('Only the readonly value is supported')
            if len(values) > 4:
                share = values[4]
                if share not in valid_shares:
                    raise ValueError(share + ' is not in ' + valid_shares)
        res = tmpl.format(**locals())
        if ro:
            res += ',readonly'
        if share:
            res += ',bind-propagation=' + share
        return res

    def parse_tmpfs(self, mnt):
        tmpl = '--mount=type=tmpfs,dst={dst}'
        values = mnt.split(':')
        dst = values[1]
        if len(values) > 2:
            size = int(values[2])
            if len(values) > 3:
                mode = values[3]
        res = tmpl.format(**locals())
        if size:
            res += ',tmpfs-size={}'.format(size)
        if mode:
            res += ',tmpfs-mode=' + mode
        return res

    def parse_volume(self, mnt):
        tmpl = '--mount=type=volume,src={src},dst={dst}'
        values = mnt.split(':')
        src, dst = values[1:3]
        ro = False
        if len(values) > 3:
            ro = values[3]
            if ro != 'readonly':
                raise ValueError('Only the readonly value is supported')
        res = tmpl.format(**locals())
        if len(values) > 3:
            ro = values[3]
            if ro != 'readonly':
                raise ValueError('Only the readonly value is supported')
        if ro:
            res += ',readonly'
        return res

    def from_unicode(self, string):
        values = super().from_unicode(string)
        if not values:
            return values
        converted = []
        for mnt in values:
            typ = mnt.split(':', 1)[0]
            if typ not in ('bind, tmpfs, volume'):
                raise ValueError('Unknown type in ' + mnt)
            if typ == 'bind':
                converted.append(self.parse_bind(mnt))
            elif typ == 'volume':
                converted.append(self.parse_volume(mnt))
            elif typ == 'tmpfs':
                converted.append(self.parse_tmpfs(mnt))
        return converted


class TimeoutsOption(ListOption):
    """Timeouts definition for an exponential backoff on retries."""

    def __init__(self, name, help_string, **kwargs):
        # Add help boilerplate
        help_string += '''

The (first, up_to, retries) tuple is defined as:
- first: seconds to wait after the first attempt
- up_to: seconds after which to give up
- retries: how many attempts after the first try
'''
        # Force invalid values to be an error (and forbids overriding it) to
        # catch invalid values
        super().__init__(name, help_string, invalid='error', **kwargs)

    def from_unicode(self, string):
        values = super().from_unicode(string)
        if not values:
            return values
        if len(values) != 3:
            raise ValueError('{} has invalid length: {}'.format(
                values, len(values)))
        first, up_to, retries = values
        first = float(first)
        up_to = float(up_to)
        retries = int(retries)
        return timeouts.ExponentialBackoff(first, up_to, retries)

# vm.distribution identifies a distribution by name
# vm.release identifies a release (or series) inside a distribution

######################################################################
# host options
######################################################################
register(ListOption('host.free.ports',
                    default='',
                    help_string='''\
An explicit list of free ports available on the local host.

This is mainly intended for tests which are responsible to seed the value
before consumption.

This is under user responsability and can be checked with `nmap localhost` to
ensure the ports aren't used.
'''))

######################################################################
# common vm options
######################################################################
register(Option('vm', default=None,
                help_string='''\
The name space defining a virtual machine.

This option is a place holder to document the options that defines a virtual
machine and the options defining the infrastructure used to manage them all.

For libvirt based vms, the definition of a vm is stored in an xml file under
'/etc/libvirt/qemu/{vm.name}.xml'. This is under the libvirt package control
and is out of scope for byov.

There are 3 other significant files used for a given libvirt vm:

- a disk image mounted at '/' from '/dev/sda1':
  '{libvirt.images_dir}/{vm.name}.qcow2'

- an iso image available from '/dev/sdb' labeled 'cidata':
  {libvirt.images_dir}/{vm.name}.seed which contains the cloud-init data used
  to configure/install/update the vm.

- a console: {libvirt.images_dir}/{vm.name}.console which can be 'tail -f'ed
  from the host.

The data used to create the seed above are stored in a vm specific
configuration directory for easier debug and reference:
- {vm.config_dir}/user-data
- {vm.config_dir}/meta-data
- {vm.config_dir}/ecdsa
- {vm.config_dir}/ecdsa.pub
'''))

# The directory where we store vm files related to their configuration with
# cloud-init (user-data, meta-data, ssh server keys).
register(PathOption('vm.vms_dir', default='~/.config/byov',
                    help_string='''\
Where vm related config files are stored.

This includes user-data and meta-data for cloud-init and ssh server keys.

This directory must exist.

Each vm get a specific directory (automatically created) there based on its
name.
'''))
# The VM classes are registered where/when needed
vm_class_registry = registries.Registry()


def register_vm_class(kls):
    vm_class_registry.register(kls.vm_class, kls, kls.__doc__)

register(RegistryOption('vm.class', registry=vm_class_registry,
                        default=MANDATORY,
                        help_string='''\
The virtual machine technology to use.'''))


# The ubiquitous vm name

# Internally the vm name is carried from command line to select the right vm
# configuration stack. So, unless it's overidden (which is undefined
# territory), it's always matching.  If any workflow/usage of byov is broken by
# this, it's a regression bug and a workaround will be provided if/when
# reported ;-)
def name_from_conf(conf):
    return conf.vm_name


register(Option('vm.name', default=name_from_conf, invalid='error',
                help_string='''\
The vm name, used as a prefix for related files.'''))
# FIXME: Arguably the default distribution should be None, possibly the same as
# the host -- vila 2024-07-03
# The next most important bits: distribution and release (and architecture)
register(Option('vm.distribution', default='ubuntu', invalid='error',
                help_string='''The distribution name.'''))
register(Option('vm.release', default=None, invalid='error',
                help_string='''The release name.'''))
register(Option('vm.architecture', default=None, invalid='error',
                help_string='''The vm architecture (cpu model).'''))
register(Option('vm.published_as',
                default=MANDATORY,
                help_string='''\
The name used to publish the stopped vm as an image.'''))
register(Option('vm.fqdn', default=None,
                help_string='''\
The fully qualified domain name for the vm.'''))
register(Option('vm.manage_etc_hosts', default='localhost',
                help_string='''\
Whether cloud-init should manage /etc/hosts or not.

This is rarely needed but can be set to 'localhost' to avoid conflicts with
other packages willing to modify /etc/hosts (puppet is a known case).

The default is `localhost`, refer to cloud-init documentation for details. This
was last changed (from True) to work-around an error message from
`cloud-init`. There may be a bug there in how boolean values are communicated
to `cloud-init`.
'''))

# The third important piece to define a vm: where to store files like the
# console, the user-data and meta-data files, the ssh server keys, etc.
register(PathOption('vm.config_dir', default='{vm.vms_dir}/{vm.name}',
                    invalid='error',
                    help_string='''\
The directory where files specific to a vm are stored.

This includes the user-data and meta-data files used at install time (for
reference and easier debug) as well as the optional ssh server keys.

By default this is {vm.vms_dir}/{vm.name}. You can put it somewhere else by
redefining it as long as it ends up being unique for the vm.

{vm.vms_dir}/{vm.release}/{vm.name} may better suit your taste for example.
'''))
# The options defining the vm physical characteristics
register(Option('vm.cpus', default='1', help_string='''The number of cpus.'''))
register(Option('vm.ram_size', default='2048',
                help_string='''The ram size in megabytes.'''))
register(Option('vm.disk_size', default='8G',
                help_string='''The disk image size in bytes.

Optional suffixes "k" or "K" (kilobyte, 1024) "M" (megabyte, 1024k) "G"
(gigabyte, 1024M) and T (terabyte, 1024G) are supported.
'''))
register(Option('vm.meta_data', default='''\
instance-id: {vm.name}
local-hostname: {vm.name}
''',
                invalid='error',
                help_string='''\
The meta data for cloud-init to put in the seed.'''))

register(Option('vm.user',
                default='{{vm.distribution}.user}',
                help_string='''The user in the vm.'''))
register(Option('vm.user.home', default='/home/{vm.user}',
                help_string='''\
Home directory for the user.

Rarely needed but when it cannot be guessed, a life saver.
'''))
register(Option('vm.user.shell',
                default='{{vm.distribution}.user.shell}',
                help_string='''\
The user's login shell.

The default is system/distribution/image specific.
'''))
register(Option('vm.user.system', default=False, invalid='error',
                from_unicode=options.bool_from_store,
                help_string='''\
Is {vm.user} a system user.
'''))
register(ListOption('vm.user.sudo',
                    default='ALL=(ALL) NOPASSWD:ALL',
                    help_string='''\
A list of sudo strings to be installed for {vm.user}.
'''))
# Some bits that may be added to user-data but are optional

register(ListOption('vm.chpasswd',
                    default=None,
                    help_string='''\
A list of tuples (user:pass) defining passwords.

The passwords can be hashed with mkpasswd but as the cloud-init explains: "If
you do not fully trust the medium over which your cloud-config will be
transmitted, then you should use SSH authentication only.
'''))
register(Option('vm.locale', default='en_US.UTF-8',
                help_string='''The locale to use.'''))
register(Option('vm.locale.encoding', default='UTF-8',
                help_string='''The locale encoding to use for {vm.locale}.'''))
register(Option('vm.package.manager',
                default='{{vm.distribution}.package.manager}',
                help_string='''The package manager for the vm.'''))
# FIXME: This could default to the package manager associated option
# -- vila 2021-12-30
register(PackageListOption('vm.packages', default='',
                           help_string='''\
A list of package names to be installed.

If the package name starts with '@', it is interpreted as a file name
and its content, one package by line, is inserted in the list.
'''))
register(Option('vm.update', default=False,
                from_unicode=options.bool_from_store,
                help_string='''Whether or not the vm should be updated.

Both apt-get update and apt-get dist-upgrade are called if this option is set.
'''))
register(Option('vm.poweroff', default=False,
                from_unicode=options.bool_from_store,
                help_string='''\
Whether or not the vm should stop at the end of the installation.'''))
# The options to control vm.backing reuse
register(Option('vm.setup.digest', default=None,
                help_string='''\
A digest of all option values defining the vm.

This is produced by byov itself and should not be set manually.
'''))
# FIXME: When credentials are required for some tests ({launchpad.login} or
# {gitlab.login}), special care should be taken when feeding those credentials
# into the test setups. This seeding can only occur when explicitely required
# by the user. This is the crux of the 'Ugly duck' issue: requiring test
# credentials is a step above asking to share exising user ones.
# --  vila 2024-09-07
register(ListOption('vm.setup.digest.options',
                    default='vm.name, vm.class,'
                    'vm.distribution, vm.release, vm.architecture,'
                    'vm.user, {vm.distribution}.user,'
                    'vm.user.system, vm.user.home, vm.user.sudo,'
                    'vm.fqdn, vm.manage_etc_hosts,'
                    'vm.cpus, vm.ram_size, vm.disk_size,'
                    'vm.meta_data,'
                    'vm.locale, vm.locale.encoding,'
                    'vm.packages,'
                    'pip.packages,'
                    'vm.setup.hook,'
                    'vm.start.hook,'
                    'vm.uploaded_scripts.guest_dir,'
                    'vm.final_message,'
                    'launchpad.login,'  # Ugly duck
                    'gitlab.login,'  # Ugly duck
                    '{vm.class}.setup.digest.options',
                    help_string='''\
A list of options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))
# The scripts that are executed at the end of cloud-init setup
register(PathOption('vm.root_script', default=None,
                    help_string='''\
The path to a script executed as root at the end of cloud-init setup.

This script is executed by cloud-init before {vm.user_script}.
'''))
register(PathOption('vm.user_script', default=None,
                    help_string='''\
The path to a script executed as the default user at the end of cloud-init
setup.

This script is executed by cloud-init after {vm.root_script}.
'''))
# FIXME: vm.setup.hook can run a script on host which can byov push
# files. vm.uploaded_scripts and vm.uploaded_scripts.guest_dir should be
# deprecated -- vila 2024-01-11
register(ListOption('vm.uploaded_scripts', default=None,
                    help_string='''\
A list of scripts to be uploaded to the guest.

Scripts can use config options from their vm, they will be expanded before
upload. All scripts are uploaded into {vm.uploaded_scripts.guest_dir} under
their base name.
'''))
register(Option('vm.uploaded_scripts.guest_dir',
                default='~{{vm.distribution}.user}/bin',
                help_string='''\
Where {vm.uploaded_scripts} are uploaded on the guest.'''))
register(Option('vm.setup.hook', default=None,
                help_string='''\
A command that is executed *on the host* at the end of the setup.

If options expansion is needed, '@script' will expand the options inside
'script' before execution.

Note: This runs after 'vm.packages' have been installed and before
'vm.setup_scripts'.
'''))
register(ListOption('vm.setup_scripts', default=None,
                    help_string='''\
A list of scripts to be executed on the guest to finalize the setup.

The scripts are executed over ssh, in the user home directory.
Scripts can use config options from their vm, they will be expanded before
upload.
'''))
register(Option('vm.final_message',
                default=None,
                help_string='''\
The cloud-init final message, a release-specific message is used if
none is provided to address compatibility with Ubuntu precise.'''))
register(Option('vm.start.hook', default=None,
                help_string='''\
A command that is executed *on the host* before starting the vm.

If options expansion is needed, '@script' will expand the options inside
'script' before execution.
'''))


def default_byov_scripts(conf):
    from importlib import resources
    return resources.files(byov).joinpath('scripts').as_posix()


register(Option('byov.scripts',
                default=default_byov_scripts,
                help_string='''\
The absolute path to the byov provided scripts.
'''))
######################################################################
# scaleway options
######################################################################
register(Option('scaleway.access_key',
                default=MANDATORY,
                help_string='''The scaleway access key.

See https://cloud.scaleway.com/#/credentials for details.
'''))
register(Option('scaleway.token',
                default=MANDATORY,
                help_string='''The scaleway authorization token.

See https://cloud.scaleway.com/#/credentials for valid ones.
'''))
register(Option('scaleway.public_ip',
                default=None,
                help_string='''The reserved ip to use.

The IP address to assign to the vm. It should be an existing reserved IP, not
already used by an existing server.
'''))
register(Option('scaleway.region_name',
                default=MANDATORY,
                help_string='''The scaleway region name.
See https://scaleway.com.
'''))
register(Option('scaleway.flavor',
                default=MANDATORY,
                help_string='''\
A scaleway commercial type for the server.

See https://scaleway.com.
'''))
register(Option('scaleway.boot.local',
                from_unicode=options.bool_from_store,
                default=None,
                help_string='''\
Boot the kernel on the first volume.

Only works for some types of server so opt-in only for now.
'''))
register(Option('scaleway.image.bootstrap',
                from_unicode=options.bool_from_store,
                default='false',
                help_string='''\
Disable cloud-init check when creating scaleway images.

Images provided by scaleway don't include cloud-init. This option disables the
checks for cloud-init completion.
'''))
# FIXME: scaleway.bootscript is missing -- vila 2018-01-24
register(Option('scaleway.image',
                default='{vm.distribution}/{vm.release}/{vm.architecture}',
                help_string='''\
The image to boot from.

See https://www.scaleway.com/imagehub/.
'''))
# It could take up to 20 mins in the worst cases (especially when creating
# several servers at once).
register(Option('scaleway.poweron_timeout', default='1800',
                from_unicode=options.float_from_store,
                help_string='''\
Max time to power on a scaleway server (in seconds).'''))
register(Option('scaleway.poweroff_timeout', default='600',
                from_unicode=options.float_from_store,
                help_string='''\
Max time to power off a scaleway server (in seconds).'''))
register(Option('scaleway.terminate_timeout', default='300',
                from_unicode=options.float_from_store,
                help_string='''\
Max time to terminate a scaleway server (in seconds).'''))
# FIXME: It takes around 3 minutes to boot and get a dynamic IP for C1, check
# whether it's faster with a static one -- vila 2018-01-14
register(TimeoutsOption('scaleway.setup_ip.timeouts',
                        default='60, 600, 20',
                        help_string='''\
When waiting for scaleway to setup an IP.'''))
register(TimeoutsOption('scaleway.setup_ssh.timeouts', default='0, 180, 20',
                        help_string='''\
When waiting for scaleway to setup ssh.'''))
register(TimeoutsOption('scaleway.cloud_init.timeouts', default='0, 240, 20',
                        help_string='''\
When waiting for cloud-init completion.
'''))
register(ListOption('scaleway.setup.digest.options',
                    default='scaleway.flavor, scaleway.image,'
                    'scaleway.bootscript, scaleway.isntance_id',
                    help_string='''\
A list of scaleway related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))
register(Option('scaleway.compute.url',
                default='https://cp-{scaleway.region_name}.scaleway.com',
                help_string='''The scaleway compute api url.

See https://developer.scaleway.com.
'''))
register(TimeoutsOption('scaleway.compute.timeouts',
                        default='2, 30, 10',
                        help_string='''\
When talking to the scaleway compute server.'''))

######################################################################
# qemu options
######################################################################

register(PathOption('qemu.image',
                    default='''{qemu.images.dir}/vms/{vm.name}''',
                    help_string='''\
The path where the boot image is stored.

This defines the name space for the vms disk images using the vm name.

Most image commands end up producing an image in that name space.
'''))

register(ListOption('qemu.image.setup',
                    default='download,convert,resize',
                    help_string='''\
A list of qemu image commands to execute before setup.

Supported commands (see corresponding help): {qemu.download}, {qemu.convert},
{qemu.clone}, {qemu.copy}, {qemu.create}, {qemu.resize}.
'''))
register(ListOption('qemu.image.teardown',
                    default='convert',
                    help_string='''\
A list of qemu image commands to execute after teardown. The commands accepted
are the same as for {qemu.image.setup} but they are executed in the reverse
order at teardown time.

Depending on the workflow, .setup and .teardown can be different to give
flexibility. Using 'download,clone' for setup and 'clone' for teardown will
keep the downloaded images after the first download. Using 'download,clone' in
teardown will force a re-download.
'''))

register(Option('qemu.download.url',
                default='{{vm.distribution}.qemu.download.url}',
                help_string='''\
The url where the image can be downloaded from.'''))
register(PathOption('qemu.download.dir',
                    default='~/.cache/byov/images',
                    help_string='''Where downloads end up.'''))
register(PathOption('qemu.download.path',
                    default='''\
{qemu.download.dir}/{vm.distribution}/{vm.release}-{vm.architecture}''',
                            help_string='''\
The path where the image is downloaded.

This defines the name space for the downloads using distribution, release and
architecture.
'''))

register(ListOption('qemu.clone', separator=' ',
                    default='''\
qemu-img create -f qcow2 -F qcow2 -b {source} {target}''',
                            help_string='''\
Create target ({qemu.image}) on top of source ({vm.published_as}
in {vm.backing}).
'''))
register(ListOption('qemu.convert', separator=' ',
                    default='''\
qemu-img convert -O qcow2 {source} {target}''',
                    help_string='''\
Convert source ({qemu.download.path}) into target ({qemu.image}).
'''))
register(ListOption('qemu.copy', separator=' ',
                    default='''\
cp {source} {target}''',
                            help_string='''\
Copy source ({qemu.download.path}) into target ({qemu.image}).
'''))
register(ListOption('qemu.create', separator=' ',
                    default='''\
qemu-img create -f qcow2 {target} {vm.disk_size}''',
                    help_string='''\
Create image at target ({qemu.image}).
'''))
register(ListOption('qemu.download', separator=' ',
                    default='''\
wget {source} -nv --output-document {target}''',
                    help_string='''\
Downloads source ({qemu.download.url}) into target ({qemu.download.path}).
The download does not happen if {qemu.download.path} already exists.
'''))
# FIXME: Could each command define its own env so run_cmd() can use
# that instead of the hard-coded source/target ? -- vila 2019-12-07

# Abusing {source} to give access to disk size
register(ListOption('qemu.resize', separator=' ',
                    default='''\
qemu-img resize {target} {source}''',
                            help_string='''\
Resize image at target ({qemu.image}) with source ({vm.disk_size}).
'''))
register(ListOption('qemu.uefi.vars', separator=' ',
                    default='''\
cp {source} {target}''',
                            help_string='''\
Seed uefi variables for the vm ({qemu.uefi.vars.path}) with source
({qemu.uefi.vars.seed}).
'''))
register(PathOption('qemu.images.dir',
                    default='~/.local/share/byov',
                    help_string='''\
Where qemu vm disk images are stored.'''))

# UEFI related options

register(PathOption('qemu.uefi.vars.seed',
                    default='/usr/share/OVMF/OVMF_VARS_4M.fd',
                    help_string='''\
The default values for UEFI variables.
Provided by the ovmf package.
'''))
register(PathOption('qemu.uefi.vars.path',
                    default='{qemu.image}-OVMF_VARS_4M.fd',
                    help_string='''\
The UEFI variables specific to the vm.

The defaults values are provided by the ovmf package.

Add `uefi.vars` in `qemu.image.setup` and `qemu.image.teardown` to set/reset
them at setup/teardown.
'''))
register(PathOption('qemu.uefi.code.path',
                    default='/usr/share/OVMF/OVMF_CODE_4M.fd',
                    help_string='''\
The default UEFI code.
Provided by the ovmf package.
'''))
register(ListOption('qemu.disks.uefi.code', separator=' ',
                    default='''\
-drive if=pflash,format=raw,readonly,file={qemu.uefi.code.path}''',
                    help_string='''\
The drive qemu option containing the uefi code.
'''))
register(ListOption('qemu.disks.uefi.vars', separator=' ',
                    default='''\
-drive if=pflash,format=raw,file={qemu.uefi.vars.path}''',
                    help_string='''\
The drive qemu option containing the vm-specifics uefi variables.
'''))

register(ListOption('qemu.disks.uefi', separator=' ',
                    default='''\
{qemu.disks.uefi.code} {qemu.disks.uefi.vars}''',
                    help_string='''\
The drives qemu option containing uefi code and variables.
'''))

# FIXME: Shouldn't the default be -drive if=virtio,file={qemu.image} ?
# -- vila 2024-01-05
register(ListOption('qemu.disks', separator=' ',
                    default='',
                    help_string='''\
Additional disks definitions.

This is added to the qemu command under user responsibility after
the default -drive if=virtio,file={qemu.image}.
'''))

# https://wiki.archlinux.org/index.php/QEMU#User-mode_networking has all the
# good bits about network setup for qemu
# https://virt.kernelnewbies.org/MacVTap for macvtap
# https://seravo.fi/2012/virtualized-bridged-networking-with-macvtap
# https://turlucode.com/qemu-kvm-bridged-networking/
# https://wiki.archlinux.org/index.php/QEMU#Bridged_networking_using_qemu-bridge-helper
register(ListOption('qemu.networks', separator=' ',
                    default='''\
-device e1000,netdev=user.0 \
-netdev user,id=user.0,hostfwd=tcp::{qemu.ssh.localhost.port}-:22''',
                    help_string='''\
The network definitions provided to qemu.

This can be specialized for each machine but the default should work for all
setups with the caveat that only ssh access is provided by forwarding a
localhost port (qemu.ssh.localhost.port) that needs to be set.

Alternatively, a bridge (br0 below) can be created on the host. From there,
qemu.networks can be set to:

  qemu.networks = -net bridge,br=br0 -net nic,macaddr=xx:xx:xx:xx:xx:xx

'''))
register(Option('qemu.ssh.localhost.port', default=None,
                help_string='''\
When set, ssh connect to localhost on that port.

This redirection should appear in qemu.networks.
'''))
register(Option('qemu.bridge', default=None,
                help_string='''\
To use in qemu.networks when a bridge is available on the host as:

  -net bridge,br={qemu.bridge} -net nic,macaddr={qemu.mac.address}

'''))

register(PathOption('qemu.bridge.helper',
                    default='/usr/lib/qemu/qemu-bridge-helper',
                    help_string='''The path to the qemu-bridge-helper program.

This should provide the user with the ability to use a bridge.  Using a bridge
means users can allocate IPs to their qemu machines. qemu uses this helper
internally and the only known way to give users access it the sticky
bit... Possibly a bit dirty but better than sudo'ing the whole qemu call.'''))


def mac_from_pid(conf):
    """Create a MAC local address based on the process id.

    Assuming /proc/sys/kernel/pid_max requires at most 7 digits (4.194.304 is
    linux default), the last 7 bytes of the mac address can be mapped to pid
    digits (leaving all the a-f combinations free for other uses).
    """
    digits = []
    remain = pid = os.getpid()
    for _ in range(4):
        digit = int(remain % 100)
        digits.insert(0, digit)
        remain = int((remain - digit) / 100)
    # FIXME: May be the formatting could happen during conversion from unicode
    # so that a /mask/ of '0e:' could be used to mean: gimme a MAC address
    # starting with. Or use 0e:0P:PP:II:DD asking PID to be replaced
    # -- vila 2019-09-16
    prefix = conf.get('qemu.mac.prefix')
    mac_format = prefix + '{:02d}:' * 4
    mac_address = mac_format.format(*digits)
    logger.debug('{} got MAC {} for pid {}'.format(
        conf.get('vm.name'), mac_address, pid))
    return mac_address


register(Option('qemu.mac.address', default=mac_from_pid,
                help_string='''\
To use in qemu.networks when a bridge is available on the host as:

  -net bridge,br={qemu.bridge} -net nic,macaddr={qemu.mac.address}

https://en.wikipedia.org/wiki/MAC_address documents local MAC addresses.
'''))
register(Option('qemu.mac.prefix', default='0e:',
                help_string='''\
This is used when creating a MAC address from the current process id.

The default value for qemu.mac.address uses this prefix.
'''))
register(ListOption('qemu.ip.neighbour.command',
                    default='ip, -c=never, neighbour, '
                    'show, dev, {qemu.bridge}',
                    help_string='''\
This is used to capture the IP address as soon as possible.
'''))
register(ListOption('qemu.ip.ping.command',
                    default='ping, -4, -c1, {vm.name}',
                    help_string='''\
This is used to ping {vm.name} to reveal its IP as soon as possible. Used in
conjonction with qemu.ip.neighbour.command.
'''))
register(ListOption('qemu.graphics', separator=' ',
                    default='-nographic',
                    help_string='''\
The options defining the qemu graphic setup.
'''))
register(TimeoutsOption('qemu.setup_ip.timeouts', default='0, 600, 60',
                        help_string='''\
When waiting for qemu to setup an IP address.'''))
register(TimeoutsOption('qemu.setup_ssh.timeouts', default='0, 120, 10',
                        help_string='''When waiting for qemu to setup ssh.'''))
register(TimeoutsOption('qemu.init.timeouts', default='10, 60, 10',
                        help_string='''When waiting for qemu to start.'''))
register(TimeoutsOption('qemu.cloud_init.timeouts', default='0, 240, 20',
                        help_string='''\
When waiting for cloud-init completion.'''))
register(TimeoutsOption('qemu.stop.timeouts', default='0, 60, 10',
                        help_string='''When waiting for qemu to stop.'''))
register(Option('qemu.pid',
                default=None,
                from_unicode=options.int_from_store,
                help_string='''The qemu process id when running.'''))

register(ListOption('qemu.setup.digest.options',
                    default='qemu.mac_address, qemu.image,'
                    'qeum.image.setup, qeum.image.teardown,'
                    'qemu.download.url, qemu.download.path'
                    'qemu.graphics, qemu.networks, qemu.disks',
                    help_string='''\
A list of qemu related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))

######################################################################
# nova options
######################################################################
register(Option('nova.username', default_from_env=['OS_USERNAME'],
                default=MANDATORY,
                help_string='''The Open Stack user name.

This is generally set via OS_USERNAME, sourced from a novarc file
(~/.novarc, ~/.canonistack/novarc).
'''))
register(Option('nova.password', default_from_env=['OS_PASSWORD'],
                default=MANDATORY,
                help_string='''The Open Stack password.

This is generally set via OS_PASSWORD, sourced from a novarc file
(~/.novarc, ~/.canonistack/novarc).
'''))
register(Option('nova.region_name',
                default_from_env=['OS_REGION_NAME'],
                default=MANDATORY,
                help_string='''The Open Stack region name.

This is generally set via OS_REGION_NAME, sourced from a novarc file
(~/.novarc, ~/.canonistack/novarc).
'''))
register(Option('nova.tenant_name',
                default_from_env=['OS_TENANT_NAME'],
                default=MANDATORY,
                help_string='''The Open Stack tenant name.

This is generally set via OS_TENANT_NAME, sourced from a novarc file
(~/.novarc, ~/.canonistack/novarc).
'''))
register(Option('nova.auth_url', default_from_env=['OS_AUTH_URL'],
                default=MANDATORY,
                help_string='''The Open Stack keystone url.

This is generally set via OS_AUTH_URL, sourced from a novarc file
(~/.novarc, ~/.canonistack/novarc).
'''))
register(ListOption('nova.flavors', default=None,
                    help_string='''\
A list of flavors for all supported clouds.

The first known one is used.
'''))
register(Option('nova.image', default=MANDATORY,
                help_string='''The glance image to boot from.'''))
register(Option('nova.net_id', default=None,
                help_string='''The network id for the vm.'''))

register(Option('nova.boot_timeout', default='600',
                from_unicode=options.float_from_store,
                help_string='''\
Max time to boot a nova instance (in seconds).'''))
register(TimeoutsOption('nova.setup_ip.timeouts', default='0, 120, 10',
                        help_string='''\
 When waiting for nova to setup an IP.'''))
register(TimeoutsOption('nova.setup_ssh.timeouts', default='0, 120, 10',
                        help_string='''When waiting for nova to setup ssh.'''))
# FIXME: 600 is a more realistic value but canonistack can be really slow and
# 3600 has been observed. There should be a better way to declare default
# values on a per cloud basis -- vila 2015-12-21
register(Option('nova.cloud_init_timeout', default='3600',
                from_unicode=options.float_from_store,
                help_string='''\
Max time for cloud-init to finish (in seconds).'''))
register(ListOption('nova.setup.digest.options',
                    default='nova.username, nova.password,'
                    'nova.region_name, nova.tenant_name, nova.image,'
                    'nova.flavors',
                    help_string='''\
A list of nova related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))

######################################################################
# aws ec2 options
######################################################################
register(Option('aws.key',
                default=MANDATORY,
                help_string='''The aws access key id.'''))
register(Option('aws.secret',
                default=MANDATORY,
                help_string='''The aws secret access key.'''))
register(Option('aws.region',
                default=MANDATORY,
                help_string='''The aws region name.'''))
register(ListOption('ec2.instance.types', default='t2.micro',
                    help_string='''\
A list of instance types to choose from.

The first known one is used.
'''))
register(Option('ec2.free_tier',
                default=True,
                from_unicode=options.bool_from_store,
                help_string='''\
Only select free tier instance types.'''))
# The image regexp for a given distribution
ec2_image_re_registry = registries.Registry()

register(RegistryOption('ec2.distribution.images',
                        registry=ec2_image_re_registry,
                        help_string='''\
The image regexp to use to select an image for a given distribution.'''))
ec2_image_re_registry.register(
    'ubuntu',
    '^ubuntu/images/hvm-ssd/ubuntu-{vm.release}-.*-{vm.architecture}-server.*',
    'Ubuntu images AMI regexp.')
ec2_image_re_registry.register(
    'amazon',
    '^amzn{vm.release}-ami-ecs-hvm-.*-ebs',
    'Amazon Linux images AMI regexp.')
ec2_image_re_registry.register(
    'debian',
    '^debian-{vm.release}-{vm.architecture}-.*',
    'Debian images AMI regexp.')

# FIXME: Could this handle re.compile as part as its default function ? (See
# Ec2Server.find_ec2_image for context) -- vila 2024-11-05
register(Option('ec2.image', default=MANDATORY,
                help_string='''\
The image regexp to select images.

If this is not set, {vm.distribution} is used to select the right regexp from
{ec2.distribution.images}.
'''))
register(Option('ec2.image.id', default=None,
                help_string='''The AMI id to boot from.

This helps disambiguate {ec2.image} by providing a unique AMI id.
'''))
register(ListOption('ec2.image.tags', separator=' ',
                    default='',
                    help_string='''\
A flatten list of key, value pairs to set as tags on the created image.
'''))
register(ListOption('ec2.image.owners', default='',
                    help_string='''\
The image owners to filter image candidates.

A distribution specific default value is used if not set.
'''))
register(options.Option('ec2.instance.id',
                        default=None,
                        help_string='''The ec2 instance id.'''))
register(ListOption('ec2.instance.tags', separator=' ',
                    default='',
                    help_string='''\
A flatten list of key, value pairs to set as tags on the created instance.
'''))
register(Option('ec2.published.id',
                default=None,
                help_string='''The published image id.
This is available as long as the instance is not terminated and is required
to unpublish a previously published image.
'''))
register(Option('ec2.subnet', default=options.MANDATORY,
                help_string='''\
The subnet id for the vm.'''))
register(ListOption('ec2.security.groups', default=options.MANDATORY,
                    help_string='''\
The security groups for the vm.'''))
register(TimeoutsOption('ec2.boot.timeouts', default='10, 900, 60',
                        help_string='''\
When waiting for ec2 to boot.'''))
register(TimeoutsOption('ec2.setup_ip.timeouts', default='10, 240, 20',
                        help_string='''\
When waiting for ec2 to setup an IP.'''))
register(TimeoutsOption('ec2.setup_ssh.timeouts', default='0, 120, 10',
                        help_string='''When waiting for ec2 to setup ssh.'''))
register(TimeoutsOption('ec2.cloud_init.timeouts', default='0, 120, 20',
                        help_string='''\
When waiting for cloud-init completion.
'''))
register(TimeoutsOption('ec2.stop.timeouts', default='0, 240, 20',
                        help_string='''When waiting for ec2 to stop.'''))
register(TimeoutsOption('ec2.terminate.timeouts', default='0, 240, 20',
                        help_string='''When waiting for ec2 to terminate.'''))
register(TimeoutsOption('ec2.create_image.timeouts', default='0, 1200, 120',
                        help_string='''\
When waiting for ec2 to create an image.'''))
register(ListOption('ec2.setup.digest.options',
                    default='aws.key, aws.secret,'
                    'aws.region, ec2.type, ec2.image, ec2.image.id,'
                    'ec2.subnet',
                    help_string='''\
A list of ec2 related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))
######################################################################
# lxd options
######################################################################

# MISSINGTESTS: vila 2023-10-11 Test the ../scripts/first_use/*lxd scripts
# using the following `lxd.install.*` options. Separating the uninstall was not
# enough to iterate safely, this needs to happen in a proper lxd container or
# even in a qemu for the zfs specific bits.

register(PackageListOption('lxd.install.packages', default='lxd, lxd-client',
                           help_string='''\
A list of package names to be installed to get a proper lxd setup.

If the package name starts with '@', it is interpreted as a file name
and its content, one package by line, is inserted in the list.
'''))
register(Option('lxd.install.storage.backend',
                default=None,
                help_string='''The storage driver for lxd.'''))
register(Option('lxd.install.storage.pool',
                default=None,
                help_string='''The pool name for lxd.'''))
register(Option('lxd.install.storage.device',
                default=None,
                help_string='''The zfs pool device for lxd.'''))


# FIXME: Using None as a default value fails
# byov.tests.test_lxd.TestInit.test_unknown_image. This needs
# investigation. Using [] as the default value works around the issue. This is
# a byoc issue and could be addressed by relaxing the constraint around
# unknown options (currently failing) that could be left as-is. The fallouts
# are unclear though.  -- vila 2016-07-12
register(ListOption('lxd.profiles', default=[],
                    help_string='''\
The profile names to apply to the container.
If empty, lxd will use the default one.

Beware of not using cloud-init in the profiles as this would conflict with
byov itself.
'''))
# FIXME: Some underlying options are missing. The format used to create the
# proxy definition should at least be exposed. -- vila 2024-11-13
register(ListOption('lxd.proxies', default=[],
                    help_string='''\
A list of ports, interpreted as (protocol, host port, vm port).

This creates one proxy device per pair, redirecting the host port into the vm
port.

Note: Only the 'tcp' protocol value has been tested.

If empty, (default), no proxies are created.
'''))
register(Option('lxd.host.listen',
                default='0.0.0.0',
                help_string='''\
The interface the host listens on for {lxd.proxies}.'''))
register(Option('lxd.vm.listen',
                default='127.0.0.1',
                help_string='''\
The interface the vm listens on for {lxd.proxies}.'''))
register(Option('lxd.image',
                default='{{vm.distribution}.lxd.image}',
                help_string='''The lxd image to boot from.'''))
register(Option('lxd.mac.address',
                default=None,
                help_string='''The MAC address to use.
This is intended to support stable IP addresses. Use with care.'''))
register(Option('lxd.remote',
                default=None,
                help_string='''The lxd remote server to use.'''))
# FIXME: Arguably the lxd.config namespace should automatically set all the
# corresponding lxd config options -- vila 2018-04-24
# FIXME: Should there be a namespace for the vms and one for the server
# (arguably the server can be addressed as a vm ? -- vila 2024-09-18
register(Option('lxd.config.boot.autostart',
                default=False,
                from_unicode=options.bool_from_store,
                help_string='''\
Should the container be started at host boot.
'''))
register(TimeoutsOption('lxd.setup_ip.timeouts', default='0, 360, 90',
                        help_string='''\
When waiting for lxd to setup an IP.'''))
register(TimeoutsOption('lxd.setup_ssh.timeouts', default='0, 120, 60',
                        help_string='''When waiting for lxd to setup ssh.'''))
register(TimeoutsOption('lxd.cloud_init.timeouts', default='0, 120, 10',
                        help_string='''\
When waiting for cloud-init completion.'''))
register(LxdUserMountsOption('lxd.user_mounts', default=None,
                             help_string='''\
A list of '<host path>:<vm path>' to be mounted.

'host' paths can start with '~' which will be expanded to the user home
directory.
Relative 'host' paths are from the current directory.

'vm' paths must be absolute.

The host paths will be available at the vm paths with the user uid/gid access
rights.

Note: This requires /etc/subuid and /etc/subgid to contain a 'root:<id>:1' line
with id being the correct user (and group) id (i.e. the user running the
'byovm setup' command).
'''))
register(PathOption('lxd.idmap.path',
                    help_string='''\

The path describing the id map provided to lxd. Syntax and examples at
https://documentation.ubuntu.com/lxd/en/latest/userns-idmap/ .

If it's prefixed by `@`, variables are expanded.
'''))
register(Option('lxd.user_mounts.host.uid',
                default=os.getuid(),
                help_string='''The host uid owning the mounts.'''))
register(Option('lxd.user_mounts.host.gid',
                default=os.getuid(),
                help_string='''The host gid owning the mounts.'''))
# '1000' is the default uid/gid in ubuntu and debian for the default vm user
# FIXME: So the default value should be provided by the distribution ?
# -- vila 2024-12-23
register(Option('lxd.user_mounts.container.uid',
                default='1000',
                help_string='''The container uid using the mounts.'''))
register(Option('lxd.user_mounts.container.gid',
                default='1000',
                help_string='''The container gid using the mounts.'''))
register(Option('lxd.privileged', default=False, invalid='error',
                from_unicode=options.bool_from_store,
                help_string='''\
Is the container privileged ?
'''))
register(Option('lxd.nesting', default=0, invalid='error',
                from_unicode=options.int_from_store,
                help_string='''\
How many level of nesting containers should be allowed for the vm.

This is used to configure the container for allowing nesting containers and
check that the /etc/subuid and /etc/subgid files provision enough ids for the
nested containers.

'0' means no nested containers.

Note that an unprivileged container can create nested privileged containers
which cannot compromise the host.
'''))
# FIXME: There is a set of options that is common between lxd and
# ephemeral-lxd. It should be defined (and used) as such. -- vila 2024-09-07
register(ListOption('lxd.setup.digest.options',
                    default='lxd.profiles, lxd.image, lxd.mac.address,'
                    'lxd.nesting, lxd.config.boot.autostart,'
                    'lxd.user_mounts,'
                    'lxd.user_mounts.host.uid,'
                    'lxd.user_mounts.host.gid,'
                    'lxd.user_mounts.container.uid,'
                    'lxd.user_mounts.container.gid,'
                    'lxd.remote',
                    help_string='''\
A list of lxd related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))
register(ListOption('ephemeral-lxd.setup.digest.options',
                    default='vm.backing,'
                    'lxd.user_mounts,'
                    'lxd.user_mounts.host.uid,'
                    'lxd.user_mounts.host.gid,'
                    'lxd.user_mounts.container.uid,'
                    'lxd.user_mounts.container.gid,'
                    'lxd.remote',
                    help_string='''\
A list of lxd related options that are used to define an ephemeral vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))


######################################################################
# docker options
######################################################################
def docker_basedir_from_conf(conf):
    dfile = subprocesses.which(conf.get('docker.file'),
                               byov.path, mode=os.F_OK)
    ddir = [root for root in byov.path if dfile.startswith(root)][0]
    return ddir


register(Option('docker.file',
                default='./Dockerfile',
                help_string='''\
The docker file to build the image.'''))
register(Option('docker.base',
                default=docker_basedir_from_conf,
                help_string='''\
The base directory for {docker.file} and {docker.mounts}.

Must be consistent with {docker.file} so relative paths are properly
interpreted.
'''))
register(Option('docker.file.expanded',
                default=None,
                help_string='''\
The option expanded docker file to build the image.'''))
register(Option('docker.image',
                default='{{vm.distribution}.docker.image}',
                help_string='''The docker image name.'''))
register(Option('docker.container.id',
                default=None,
                help_string='''The docker container id.'''))
register(Option('docker.image.id',
                default=None,
                help_string='''The docker image id.'''))
register(Option('docker.registry.name',
                default='test-registry',
                help_string='''\
The docker image registry container name.'''))
register(Option('docker.registry.host',
                default='localhost',
                help_string='''The docker image registry host.'''))
register(Option('docker.registry.port',
                default='5000',
                from_unicode=options.int_from_store,
                help_string='''The docker image registry port.'''))
register(ListOption('docker.registry.command',
                    default=('docker, run, -d, '
                             '-p, {docker.registry.port}:5000,'
                             ' --name, {docker.registry.name}, registry:2'),
                    help_string='''\
docker command to run an image test registry.'''))
register(Option('docker.create.image.hook', default=None,
                help_string='''\
A command that is executed *on the host* before building the image.

If options expansion is needed, '@script' will expand the options inside
'script' before execution.
'''))
register(ListOption('docker.image.build.command',
                    default='docker, image, build',
                    help_string='''\
Docker command to build the container image.  byov will append --quiet, --file
{docker.file} and the right working directory.
'''))
register(ListOption('docker.container.create.command',
                    default='docker, container, create',
                    help_string='''docker command to create a container.'''))
register(ListOption('docker.ports',
                    default=None,
                    help_string='''\
Docker ports list as outside:inside pairs.'''))
register(DockerMountsOption(
    'docker.mounts', default=None,
    help_string='''\
A list of docker mount definitions (tuples using ':' as a separator)
- type must be either bind, tmpfs or volume.

See https://docs.docker.com/storage/bind-mounts/ for details.

Examples:
 bind:~/src:/src:readonly:slave
 tmpfs:/tmp:65536:1777  (size and chmod bits)
 volume:volname:/mnt
'''))
register(ListOption('docker.container.start.command',
                    default='docker, container, start, {vm.name}',
                    help_string='''docker command to start the container.'''))
register(ListOption('docker.setup.done',
                    default='/bin/true',
                    help_string='''\
Command succeeding inside the container when it's ready to be used.'''))
register(TimeoutsOption(
    'docker.setup.timeouts',
    default='0, 0, 1',
    help_string='''When waiting for {docker.setup.done} to succeed.'''))
register(ListOption('docker.container.shell.command',
                    default='docker, container, exec, -i',
                    help_string='''\
docker command to run a command in the container.'''))
register(ListOption('docker.container.stop.command',
                    default=('docker, container, stop,'
                             ' --time, {docker.container.stop.timeout},'
                             ' {vm.name}'),
                    help_string='''\
docker command to stop the container.'''))
register(Option('docker.container.stop.timeout',
                default='10',
                help_string='''\
Seconds to wait for stop before killing the container.'''))
register(ListOption('docker.image.tag.command',
                    default=('docker, image, tag, {docker.image.id}, '
                             ' {docker.registry.host}:{docker.registry.port}'
                             '/{docker.image}'),
                    help_string='''\
docker command to tag an image for publication.'''))
register(ListOption('docker.image.publish.command',
                    default=('docker, image, push, '
                             '{docker.registry.host}:{docker.registry.port}'
                             '/{docker.image}'),
                    help_string='''docker command to publish an image.'''))
register(ListOption('docker.image.unpublish.command',
                    default=('docker, image, rm, -f,'
                             '{docker.registry.host}:{docker.registry.port}'
                             '/{docker.image}'),
                    help_string='''docker command to unpublish an image.'''))
register(ListOption('docker.container.teardown.command',
                    default='docker, container, rm, {vm.name}',
                    help_string='''\
docker command to teardown the container.'''))
register(ListOption('docker.container.cp.command',
                    default='docker, container, cp',
                    help_string='''\
docker command to copy a file to/from a container.'''))
register(ListOption('docker.setup.digest.options',
                    default=('docker.file,'
                             'docker.file.expanded,'
                             'docker.setup.done,'
                             'docker.image, docker.image.id'
                             'docker.ports, docker.mounts,'
                             'docker.container.cp.command,'
                             'docker.container.create.command,'
                             'docker.container.shell.command,'
                             'docker.container.start.command,'
                             'docker.container.stop.command,'
                             'docker.container.teardown.command,'
                             'docker.image.build.command,'
                             'docker.image.publish.command,'
                             'docker.image.registry.command,'
                             'docker.image.tag.command,'
                             'docker.image.unpublish.command,'),
                    help_string='''\
A list of docker related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))

######################################################################
# apt options
######################################################################

register(ListOption('apt.command',
                    default=('sudo, env, DEBIAN_FRONTEND=noninteractive,'
                             ' apt-get, {apt.options}'),
                    help_string='''apt-get command.'''))
register(ListOption('apt.options',
                    default='--option=Dpkg::Options::=--force-confold,'
                    ' --option=Dpkg::Options::=--force-unsafe-io,'
                    ' --assume-yes, --quiet, --no-install-recommends',
                    help_string='''apt-get install options.'''))
register(Option('apt.proxy', default=None, invalid='error',
                help_string='''\
A local proxy for apt to cache .deb downloads.

Example:

  apt.proxy = http://192.168.0.42:3142
'''))
register(ListOption('apt.sources', default=None,
                    help_string='''\
A list of apt sources entries to be added to the default ones.

Cloud-init already setup /etc/apt/sources.list with appropriate entries. Only
additional entries need to be specified here.
'''))
register(ListOption('apt.update.timeouts',
                    default='15.0, 90.0, 240.0',
                    help_string='''apt-get update timeouts in seconds.

When apt-get update fails on hash sum mismatches, retry after the specified
timeouts. More values mean more retries.
'''))
register(ListOption('apt.upgrade.timeouts',
                    default='15.0, 90.0, 240.0',
                    help_string='''\
apt-get dist-upgrade timeouts in seconds.

When apt-get fails with retcode 100 (Could not get lock /var/lib/dpkg/lock),
retry after the specified timeouts. More values mean more retries.
'''))
register(ListOption('apt.setup.digest.options',
                    default='apt.options, apt.sources',
                    help_string='''\
A list of apt related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))

# FIXME: Needs a way to disable apt-get dist-upgrade which is breaking for
# ubuntu trusty libssl -- vila 2016-09-10

######################################################################
# pip options
######################################################################
register(ListOption('pip.command',
                    default='pip3, {pip.options}',
                    help_string='''pip command.'''))
register(ListOption('pip.install.command',
                    default='install, --user',
                    help_string='''pip install command.

byov will append {pip.packages}'''))
register(ListOption('pip.options', default='',
                    help_string='''pip options.'''))
# FIXME: This probably needs a specific option type to support pip specifics
# (-r <file> at least) -- vila 2021-12-30
register(PackageListOption('pip.packages', default='',
                           help_string='''\
A list of package specifiers to be installed.

If the package name starts with '@', it is interpreted as a file name
and its content, one package by line, is inserted in the list.
pip packages are installed after {vm.setup_scripts} have been executed.
'''))
register(ListOption('pip.setup.digest.options',
                    default='pip.options, pip.install.command, '
                    'pip.packages',
                    help_string='''\
A list of pip related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))

######################################################################
# dnf options
######################################################################
register(ListOption('dnf.command',
                    default='sudo, dnf, {dnf.options}',
                    help_string='''dnf command.'''))
register(ListOption('dnf.options', default='-y',
                    help_string='''dnf options.'''))
register(PackageListOption('dnf.packages', default='',
                           help_string='''\
A list of package specifiers to be installed.

If the package name starts with '@', it is interpreted as a file name
and its content, one package by line, is inserted in the list.
'''))
register(ListOption('dnf.upgrade.timeouts',
                    default='15.0',
                    help_string='''\
dnf upgrade timeouts in seconds.

When dnf fails, retry after the specified timeouts.
More values mean more retries.
'''))
register(ListOption('dnf.setup.digest.options',
                    default='pip.options',
                    help_string='''\
A list of pip related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))

######################################################################
# ssh options
######################################################################
register(ListOption('ssh.server_keys', default=None,
                    help_string='''\
A list of paths to server ssh keys.

Both public and private keys can be provided. Accepted server ssh key types are
rsa and ecdsa. The file names should match <type>.*[.pub].
'''))
# FIXME: There is a tension between providing a default value and making sure
# the user understand the need for an ssh key used to connect to the vms and
# its public counterpart needed to be in ssh.authorized_keys for the vm to
# accept connections. Having a password-less key or relying on a user agent is
# another question that the user needs to answer as there is no good default
# value for that either. -- vila 2016-07-07. A passwordless (or not for that
# matter) dedicated key under ~/.config/byov sounds like the most elegant
# solution and can already be achieved by setting 'ssh.key' in the user config
# file -- vila 2016-07-22
register(PathOption('ssh.key', default='~/.ssh/id_rsa',
                    help_string='''\
The ssh key path used to access the guest.

'ssh.authorized_keys' is expected to contain the .pub companion.
'''))
register(ListOption('ssh.authorized_keys',
                    default='{ssh.key}.pub',
                    help_string='''\
A list of paths to public ssh keys to be authorized for {vm.user}.

The content of the paths will be added to the authorized_keys file for
{vm.user}.
'''))
register(Option('ssh.user', default='{vm.user}',
                help_string='''\
Which user should be used for ssh access.
'''))
register(Option('ssh.host', default='{vm.ip}',
                help_string='''\
Which host name or IP address should be used for ssh access.
'''))
register(Option('ssh.port', default=None,
                help_string='''\
Which port should be used for ssh access.
'''))
register(ListOption('ssh.options',
                    default='-oUserKnownHostsFile=/dev/null,'
                    '-oStrictHostKeyChecking=no,'
                    '-oIdentitiesOnly=yes,'
                    '-oIdentityFile={ssh.key}',
                    help_string='''\
A list of ssh options to be used when connecting to the guest via ssh.'''))
register(ListOption('ssh.setup.digest.options',
                    default='ssh.key, ssh.options',
                    help_string='''\
A list of ssh related options that are used to define a vm.

The values for these options are hashed to produce 'vm.setup.digest'.
'''))


######################################################################
# logging options
######################################################################
def level_from_store(s):
    val = None
    try:
        # Yes, _levelNames and _nameToLevel are private, but better use a
        # private than duplicate its content and get out of date.
        if sys.version_info < (3,):
            valid_levels = logging._levelNames
        else:
            valid_levels = logging._nameToLevel
        val = valid_levels[s.upper()]
    except KeyError:
        pass
    return val


register(Option('logging.level', default='ERROR',
                from_unicode=level_from_store,
                default_from_env=['LOG_LEVEL'],
                help_string='''\
Logging level (same as python: error, warning, info, debug).'''))

register(Option('logging.format',
                default='%(asctime)s %(levelname)s %(message)s',
                help_string='''\
Logging format (see python doc).'''))


######################################################################
# launchpad options
######################################################################
def default_lp_login(conf):
    lp_login_cmd = ['bzr', 'lp-login']
    try:
        ret, out, err = subprocesses.run(lp_login_cmd)
        return out.strip()
    # python2 doesn't provide FileNotFoundError. OSError is raised if bzr is
    # not available
    except (subprocesses.errors.CommandError, OSError):
        return getpass.getuser()


register(Option('launchpad.login', default=default_lp_login,
                help_string='''\
The launchpad login used for launchpad ssh access from the guest.

This defaults (acquired from the host) to 'bzr lp-login' or, if not set, to the
first environment variable set in LOGNAME, USER, LNAME, USERNAME.
'''))

######################################################################
# gitlab options
######################################################################


def default_gitlab_login(conf):
    gl_login_cmd = ['git', 'config', 'gitlab.login']
    try:
        ret, out, err = subprocesses.run(gl_login_cmd)
        return out.strip()
    # python2 doesn't provide FileNotFoundError. OSError is raised if git is
    # not available
    except (subprocesses.errors.CommandError, OSError):
        return getpass.getuser()


register(Option('gitlab.login', default=default_gitlab_login,
                help_string='''\
The gitlab login used for ssh access from the guest.

This defaults (acquired from the host) to 'git config gitlab.login' or, if not
set, to the first environment variable set in LOGNAME, USER, LNAME, USERNAME.
'''))

######################################################################
# distribution specific options
######################################################################


######################################################################
# debian options
######################################################################

# cloud (including qemu) images have names involving both the code name and the
# version so some help is needed to build the urls.

# Authoritative source: https://www.debian.org/releases/
debian_versions = dict(
    sid=('9999', 'sid'),
    forky=('14', 'next'),
    trixie=('13', 'testing'),
    bookworm=('12', 'stable'),
    bullseye=('11', 'oldstable'),
    buster=('10', 'eol'),
    stretch=('9', 'eol'),
    jessie=('8', 'eol'),
    wheezy=('7', 'eol'),
    squeeze=('6', 'eol'),
    lenny=('5', 'eol'),
    etch=('4', 'eol'),
    sarge=('3.1', 'eol'),
    woody=('3.0', 'eol'),
    potato=('2.2', 'eol'),
    slink=('2.1', 'eol'),
    hamm=('2.0', 'eol'),
)
register(Option('debian.user',
                default='debian',
                help_string='''The default user for debian.'''))
register(Option('debian.user.shell',
                default='/bin/bash',
                help_string='''The default shell on debian.'''))
register(Option('debian.release.stable',
                default='bookworm',
                help_string='''The stable release for debian.'''))
register(Option('debian.docker.image',
                default='debian:{vm.release}',
                help_string='''\
The debian docker image to boot from.'''))
register(Option('debian.lxd.image',
                default='debian/{vm.release}/{vm.architecture}',
                help_string='''The debian lxd image to boot from.'''))
register(Option('debian.package.manager',
                default='apt',
                help_string='''The package manager for debian.'''))


def default_debian_qemu_download_url(conf):
    # FIXME: This is incomplete as it should at least handle stable, testing
    # and bookworm -- vila 2024-09-23
    trixie = '''\
http://cloud.debian.org/images/cloud/{vm.release}/daily/latest/\
{vm.distribution}-13-generic-{vm.architecture}-daily.qcow2'''
    return trixie


register(Option('debian.qemu.download.url',
                default=default_debian_qemu_download_url,
                help_string='''\
The url where the image can be downloaded from.'''))
# FIXME: debian.qemu.download.url debian.qemu.download.path ?
# https://cloud.debian.org/images/openstack/current/ ?
# https://cloud.debian.org/images/cloud/ ?
# -- vila 2019-11-14


######################################################################
# ubuntu options
######################################################################
# cloud (including qemu) images have names involving both the code name and the
# version so some help is needed to build the urls.

# Authoritative source: https://en.wikipedia.org/wiki/Ubuntu_version_history
ubuntu_versions = dict(
    oracular=('24.10', 'testing'),
    noble=('24.04', 'lts', 'stable'),
    mantic=('23.10', 'eol'),
    lunar=('23.04', 'eol'),
    kinetic=('22.10', 'eol'),
    jammy=('22.04', 'lts', 'eol'),
    impish=('22.10', 'eol'),
    hirsute=('21.04', 'eol'),
    groovy=('21.10', 'eol'),
    focal=('20.04', 'lts', 'eol'),
    eoan=('19.10', 'eol'),
    disco=('19.04', 'eol'),
    cosmic=('18.10', 'eol'),
    bionic=('18.04', 'lts', 'eol'),
    artful=('17.10', 'eol'),
    zesty=('17.04', 'eol'),
    yaketty=('16.10', 'eol'),
    xenial=('16.04', 'lts', 'eol'),
    willy=('15.10', 'eol'),
    vivid=('15.04', 'eol'),
    utopic=('14.10', 'eol'),
    trusty=('14.04', 'lts', 'eol'),
    saucy=('13.10', 'eol'),
    raring=('13.04', 'eol'),
    quantal=('12.10', 'eol'),
    precise=('12.04', 'lts', 'eol'),
    oneric=('11.10', 'eol'),
    natty=('11.04', 'eol'),
    maverick=('10.10', 'eol'),
    lucid=('10.04', 'lts', 'eol'),
    karmic=('9.10', 'eol'),
    jaunty=('9.04', 'eol'),
    intrepid=('8.10', 'eol'),
    hardy=('8.04', 'lts', 'eol'),
    gutsy=('7.10', 'eol'),
    feisty=('7.04', 'eol'),
    edgy=('6.10', 'eol'),
    dapper=('6.06', 'lts', 'eol'),
    breezy=('5.10', 'eol'),
    hoary=('5.04', 'eol'),
    warty=('4.10', 'eol'),
)
# oracular oriole 24.10 testing
# noble numbat 24.04.1 stable lts
# jammy jellyfish 22.04.5 lts
# focal fossa 20.04.6 lts
# bionic beaver 18.04.6 lts
# xenial xerus 16.04.7 lts
# trusty tahr 14.04.6 lts

register(Option('ubuntu.user',
                default='ubuntu',
                help_string='''The default user for ubuntu.'''))
register(Option('ubuntu.user.shell',
                default='/bin/bash',
                help_string='''The default shell on ubuntu.'''))
register(Option('ubuntu.release.stable',
                default='noble',
                help_string='''The stable LTS release for ubuntu.'''))
register(Option('ubuntu.docker.image',
                default='ubuntu:{vm.release}',
                help_string='''\
The ubuntu docker image to boot from.'''))
register(Option('ubuntu.lxd.image',
                default='ubuntu:{vm.release}/{vm.architecture}',
                help_string='''The ubuntu lxd image to boot from.'''))
register(Option('ubuntu.package.manager',
                default='apt',
                help_string='''The package manager for ubuntu.'''))


def default_ubuntu_qemu_download_url(conf):
    # FIXME: This is incomplete as it should at least handle stable, testing
    # oracular and noble -- vila 2024-09-23
    default = '''\
http://cloud-images.ubuntu.com/{vm.release}/current/\
{vm.release}-server-cloudimg-{vm.architecture}.img'''
    return default

register(Option('ubuntu.qemu.download.url',
                default=default_ubuntu_qemu_download_url,
                help_string='''\
The url where the image can be downloaded from.'''))
# FIXME: ubuntu.qemu.download.url ubuntu.qemu.download.path ?
# -- vila 2019-11-14
######################################################################
# amazon options
######################################################################
register(Option('amazon.user',
                default='ec2-user',
                help_string='''The default user for amazon linux.'''))
register(Option('amazon.user.shell',
                default='/bin/bash',
                help_string='''The default shell on amazon linux.'''))
register(Option('amazon.docker.image',
                default='amazonlinux',
                help_string='''\
The amazon docker image to boot from.'''))
register(Option('amazon.lxd.image',
                default='amazonlinux/{vm.release}/{vm.architecture}',
                help_string='''The amzon lxd image to boot from.'''))
register(Option('amazon.package.manager',
                default='dnf',  # Not there yet...
                help_string='''The package manager for amazon.'''))
######################################################################
# centos options
######################################################################
register(Option('centos.user',
                default='centos',
                help_string='''The default user for centos.'''))
register(Option('centos.user.shell',
                default='/bin/bash',
                help_string='''The default shell on centos.'''))
register(Option('centos.package.manager',
                default='dnf',
                help_string='''The package manager for centos.'''))
register(Option('centos.lxd.image',
                default='images:centos/{vm.release}/cloud/{vm.architecture}',
                help_string='''The centos lxd image to boot from.'''))
######################################################################
# fedora options
######################################################################
register(Option('fedora.user',
                default='fedora',
                help_string='''The default user for fedora.'''))
register(Option('fedora.user.shell',
                default='/bin/bash',
                help_string='''The default shell on fedora.'''))
register(Option('fedora.package.manager',
                default='dnf',
                help_string='''The package manager for fedora.'''))
register(Option('fedora.lxd.image',
                default='images:fedora/{vm.release}/cloud/{vm.architecture}',
                help_string='''The fedora lxd image to boot from.'''))
