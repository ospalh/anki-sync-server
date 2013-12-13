#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

"""
Controller for the Anki Sync Server.
"""

from __future__ import print_function

import argparse
import binascii
import getpass
import hashlib
import os
import signal
import sqlite3
import subprocess
import sys

# SERVERCONFIG = "production.ini"
AUTHDBPATH = "auth.db"
PIDPATH = "/tmp/ankiserver.pid"
COLLECTIONPATH = "collections/"


def usage():
    print(u"""\
usage: {} <command> [<args>]


Commands:
  start [configfile] - start the server
  stop               - stop the server
  adduser <username> - add a new user
  deluser <username> - delete a user
  lsuser             - list users
  passwd <username>  - change password of a user
""".format(sys.argv[0]))


def startsrv(args):
    configfile = args.configfile

    # We change to the directory containing the config file
    # so that all the paths will be relative to it.
    configdir = os.path.dirname(configfile)
    if configdir != '':
        os.chdir(configdir)
    configfile = os.path.basename(configfile)

    devnull = open(os.devnull, "w")

    pid = subprocess.Popen(
        ["paster", "serve", configfile], stdout=devnull, stderr=devnull).pid

    with open(PIDPATH, "w") as pidfile:
        pidfile.write(str(pid))


def stopsrv(args):
    if os.path.isfile(PIDPATH):
        try:
            with open(PIDPATH) as pidfile:
                pid = int(pidfile.read())

                os.kill(pid, signal.SIGKILL)
                os.remove(PIDPATH)
        except Exception, error:
            print("{}: Failed to stop server: {}".format(
                    sys.argv[0], error.message), file=sys.stderr)
    else:
        print("{}: The server is not running".format(sys.argv[0]),
              file=sys.stderr)


def adduser(args):
    username = args.username
    if username:
        print("Enter password for {}: ".format(username))

        password = getpass.getpass()
        salt = binascii.b2a_hex(os.urandom(8))
        hash = hashlib.sha256(username+password+salt).hexdigest()+salt

        conn = sqlite3.connect(AUTHDBPATH)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS auth "
                       "(user VARCHAR PRIMARY KEY, hash VARCHAR)")

        cursor.execute("INSERT INTO auth VALUES (?, ?)", (username, hash))

        if not os.path.isdir(COLLECTIONPATH+username):
            os.makedirs(COLLECTIONPATH+username)

        conn.commit()
        conn.close()
    else:
        usage()


def deluser(args):
    username = args.username
    if username and os.path.isfile(AUTHDBPATH):
            conn = sqlite3.connect(AUTHDBPATH)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM auth WHERE user=?", (username,))

            conn.commit()
            conn.close()
    elif not username:
        usage()
    else:
        print("{}: Database file does not exist".format(sys.argv[0]),
               file=sys.stderr)


def lsuser(args):
    conn = sqlite3.connect(AUTHDBPATH)
    cursor = conn.cursor()

    cursor.execute("SELECT user FROM auth")

    row = cursor.fetchone()

    while row is not None:
        print(row[0])
        row = cursor.fetchone()
    conn.close()


def passwd(args):
    username = args.username
    if os.path.isfile(AUTHDBPATH):
        print("Enter password for "+username+": ")

        password = getpass.getpass()
        salt = binascii.b2a_hex(os.urandom(8))
        hash = hashlib.sha256(username+password+salt).hexdigest()+salt

        conn = sqlite3.connect(AUTHDBPATH)
        cursor = conn.cursor()

        cursor.execute("UPDATE auth SET hash=? WHERE user=?", (hash, username))

        conn.commit()
        conn.close()
    else:
        print("{}: Database file does not exist".format(sys.argv[0]),
              file=sys.stderr)


def main(argv):
    # create the top-level parser
    parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers(help='Commands:')
    subparsers = parser.add_subparsers()

    parser_start = subparsers.add_parser('start', help='Start the server')
    parser_start.add_argument(
        '--configfile', '-c', type=str, help='config (.ini) file to use')
    parser_start.set_defaults(func=startsrv, configfile="production.ini")

    parser_stop = subparsers.add_parser('stop', help='Stop the server')
    parser_stop.set_defaults(func=stopsrv)

    parser_adduser = subparsers.add_parser(
        'adduser', help='Add user <username>')
    parser_adduser.add_argument('username', type=str)
    parser_adduser.set_defaults(func=adduser)

    parser_deluser = subparsers.add_parser(
        'deluser', help='''Delete user <username> from the database''')
    parser_deluser.add_argument('username', type=str)
    parser_deluser.set_defaults(func=deluser)

    parser_passwd = subparsers.add_parser(
        'passwd', help='''Set the password for user <username>''')
    parser_passwd.add_argument('username', type=str)
    parser_passwd.set_defaults(func=passwd)

    # create the parser for the "b" command
    parser_lsuser = subparsers.add_parser(
        'lsuser', help='List users')
    parser_lsuser.set_defaults(func=lsuser)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
