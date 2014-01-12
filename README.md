nagios-remote-checks
=======================

Whilst the best way to create and manage your nagios checks is probably to use
something like Puppet exported resources, in some circumstances this is not
possible, such as when the nagios server has a different puppetmaster from what
it is monitoring.

Creating the Nagios checks and NRPE commands to run them is tiresome. That is
where this script comes in. If you run the script with the option 'checks', it
will generate Nagios commands to set up checks. These should be put on your
Nagios server in its configuration tree. If you run the script with the option
'commands', it will create the commands that belong in /etc/nagios/nrpe.d/ on
the machine you wish to monitor.

Configuration
-------------


Usage With xCAT
---------------

If you use xCAT you can get use the 'nodels' command to get the list of
hosts you wish to generate config for::

  nodels compute | xargs ./checkping.py checks > generated_ping_checks.cfg



Documentation for the check_ping plugin:
----------------------------------------

https://nagios-plugins.org/doc/man/check_ping.html

Usage::

  check_ping -H <host_address> -w <wrta>,<wpl>% -c <crta>,<cpl>%
   [-p packets] [-t timeout] [-4|-6]

