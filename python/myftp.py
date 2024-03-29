#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
from library import terminal, remote, command

# Parse parameters
parser = argparse.ArgumentParser(description='FTP client')
parser.add_argument('hostname', help='hostname or ip')
parser.add_argument('port', help='port info', nargs='?', default=21)
args = parser.parse_args()

# Do connect
ftp = remote.Connect()
status = ftp.connect(args.hostname, args.port)
if status == False:
    terminal.error('Connect failed')
    exit()

welcome = ftp.read()
if len(welcome) > 0:
    terminal.info('Server connected')
    terminal.info(welcome.decode().strip())
else:
    terminal.error('FTP server has no welcome message, maybe something wrong.')

# Do login
ftp.terminalLogin()
status = ftp.login(ftp.user, ftp.password)
if not status:
    exit()


# Run process
while True:
    cmd = terminal.run()
    if cmd == None:
        # Nothing input
        continue
    instance = command.getObj(cmd[0].lower())
    if instance == None:
        # Can not find out object
        terminal.error(
            'unsupported command "%s", you can input "help" to find out which command you need.' % cmd[0])
        continue
    obj = instance(ftp)
    status = obj.execute(cmd[0], cmd[1])
    if not status:
        # Parse commande failed
        continue
