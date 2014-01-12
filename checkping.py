#!/usr/bin/env python
"""
checkping.py : create nagios commands and checks to ping remote hosts via
nrpe.

"""

"""
Copyright 2013 Andrew Spiers

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import socket
import sys

if sys.version[0] == "2":
    import ConfigParser as configparser
else:
    import configparser

usage = ''.join(("usage: type 'checks' or 'commands' followed by a space ",
                "separated list of all the hosts for which you want checks ",
                "created.\n eg "))
usage += sys.argv[0]
usage += " checks host01 host02 host03"

def create_defaults():
    """return a ConfigParser object with default values in it.

    """
    # %% for safe interpolation
    main = {'check_location': '/usr/lib64/nagios/plugins/',
                        'warning_latency': '3000.0',
                        'warning_packetloss': '80%%',
                        'critical_latency': '5000.0',
                        'critical_packetloss': '100%%',
                        'contact_groups': 'systems-admins',
            }
    #default = configparser.RawConfigParser()
    default = configparser.SafeConfigParser()
    default.add_section('main')
    for key in main.keys():
        default.set('main', key, main[key])
    return default


def write_ping_check(
    hostname="server001-ipmi",
    conf=create_defaults()
                    ):
    """given a hostname, and a ConfigParser object containing the template
    to use, create the nagios command.
    """
    out = []
    indent = 2 * " "
    out.append("define service {")
    i_s = []  # indented section
    i_s.append("use generic-service")
    i_s.append("host_name " + hostname)
    i_s.append("service_description ping " + hostname)
    i_s.append("check_command check_nrpe_1arg!check_ping_" + hostname )
    i_s.append("contact_groups " + conf.get('main','contact_groups'))
    indentedpart = "\n".join([indent + i for i in i_s])
    out.append(indentedpart)
    out.append("}\n\n")
    return "\n".join(out)


def write_nrpe_ping_command(
                        hostname="server001-ipmi",
                        conf=create_defaults()
                        ):
    """given a hostname,
    return a nrpe configuration line to check that a given host is answering
    ping.

    Use a configparser obj to determine the location of the nrpe check_ping
    binary, and the warning and critical latency and packet loss threshholds.
    """
    out = "command[check_ping_"
    out += hostname
    out += ']='
    out += conf.get('main','check_location')
    out += 'check_ping -H '
    out += hostname
    out += ' -w'
    out += conf.get('main','warning_latency')
    out += ','
    out += conf.get('main','warning_packetloss')
    out += ' -c'
    out += conf.get('main','critical_latency')
    out += ','
    out += conf.get('main','critical_packetloss')
    out += "\n"
    return out


def output_checks():
  """Wrapper to call all of the checks"""
  output = ""
  output += write_ping_check()


def main():
    """do main stuff
    """
    if len(sys.argv) <= 2:
        print (usage)
        sys.exit(2)

    if sys.argv[1] == "commands":
        for i in sys.argv[2:]:
            print (write_nrpe_ping_command(hostname=i))
    elif sys.argv[1] == "checks":
        for i in sys.argv[2:]:
            print(write_ping_check(hostname=i))
    else:
        print (usage)
        sys.exit(2)


if __name__ == "__main__":
    main()
