from nose.tools import *
import sys
if sys.version_info.major < 3:
    import ConfigParser as configparser
    from StringIO import StringIO
else:
    import configparser
    from io import StringIO

import checkping

def test_create_defaults():
    d = checkping.create_defaults()
    assert_is_instance(d,configparser.RawConfigParser)

def test_defaults_not_blank():
    s = StringIO()
    checkping.create_defaults().write(s)
    s.seek(0)
    text = s.read()
    assert text != ""

def test_check_ping_command():
    desiredOutput = "command[check_ping_server001-ipmi]"
    desiredOutput += "=/usr/lib64/nagios/plugins/check_ping"
    desiredOutput += " -H server001-ipmi"
    desiredOutput += " -w3000.0,80%"
    desiredOutput += " -c5000.0,100%"
    desiredOutput += "\n"
    assert_equal(checkping.write_nrpe_ping_command('server001-ipmi'),desiredOutput)

def test_output_checks():
    assert_not_equal(checkping.output_checks(),"")

def test_write_ping_check():
    lines = ("define service {",
             "  use generic-service",
             "  host_name server001-ipmi",
             "  service_description ping server001-ipmi",
             "  check_command check_nrpe_1arg!check_ping_server001-ipmi",
             "  contact_groups systems-admins",
             "}",
             "\n",
            )
    desiredOutput = "\n".join(lines)
    assert_equal(checkping.write_ping_check('server001-ipmi'),desiredOutput)

