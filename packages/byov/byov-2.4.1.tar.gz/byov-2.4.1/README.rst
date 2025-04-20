byov: Build Your Own Virtual machine

There are a lot of ways to describe test servers as virtual machines, the
aim of the project is to make it as simple and concise as possible to keep a
complete description under version control.

This projects helps maintain throw-away virtual machines (vm) in a simple
and consistent way so they can be re-created from scratch easily and used
for tests.

It collects various recipes used to build virtual machines for different
virtualization tools (kvm, nova, scaleway, lxd, docker, ec2) and relies on
cloud-init and ssh access (except for docker).

Virtual machines are described in a configuration file capturing their
definition in a few lines and allowing image-based workflows to be defined
by chaining vms definitions.

This provides access to most of the documented options::

  `byov help` list all available help topics.

  `byov help <regexp>|` list all options matching the regexp (using topics
  as regexps works pretty well).

The next best thing is to look at `byov/options.py` where all options are
documented individually, grouped by topic (backend (nova, lxd), command
(apt, ssh) or distribution (debian, ubuntu, amazon)) among others.
