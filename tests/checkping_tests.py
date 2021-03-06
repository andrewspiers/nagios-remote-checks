from nose.tools import *
import socket
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

def test_defaults_contains_intervening_server():
    d = checkping.create_defaults()
    print (d)
    assert_equal(d.get('main','intervening_server'),socket.getfqdn())

def test_check_ping_command():
    desiredOutput = "command[check_ping_server001-ipmi]"
    desiredOutput += "=/usr/lib64/nagios/plugins/check_ping"
    desiredOutput += " -H server001-ipmi"
    desiredOutput += " -w3000.0,80%"
    desiredOutput += " -c5000.0,100%"
    desiredOutput += "\n"
    assert_equal(checkping.write_nrpe_ping_command('server001-ipmi'),desiredOutput)

def test_guess_intervening_server_normalcase():
    remote = "server001"
    intervening = "server-m"
    guess = checkping.guess_intervening_server('server001',suffix="-m")
    assert_equal(guess,intervening)

@raises (ValueError)
def test_guess_intervening_server_no_end_digit():
    remote = "server"
    checkping.guess_intervening_server(remote)

@raises(ValueError)
def test_guess_intervening_server_all_digits():
    remote = "123500"
    checkping.guess_intervening_server(remote)

def test_output_checks():
    assert_not_equal(checkping.output_checks(),"")

def test_write_ping_check():
    lines = ("define service {",
             "  use generic-service",
             "  host_name " + socket.getfqdn(),
             "  service_description ping server001-ipmi",
             "  check_command check_nrpe_1arg!check_ping_server001-ipmi",
             "  contact_groups systems-admins",
             "}",
             "\n",
            )
    desiredOutput = "\n".join(lines)
    assert_equal(checkping.write_ping_check('server001-ipmi'),desiredOutput)

