#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .. import terminal, remote
from . import base


class ls:
    '''
        ls
    '''

    ftp = None

    def __init__(self, ftp):
        '''
            init
        '''
        self.ftp = ftp

    def execute(self, cmd, params):
        '''
            execute
        '''
        # Set passive mode
        port = self.ftp.EPSV()
        if port == False:
            terminal.error('EPSV mode set failed.')
            return False

        # Connect remote data port
        dataConn = remote.Connect()
        status = dataConn.connect(self.ftp.host, port)
        if not status:
            terminal.error('Data port connect failed.')
            return False

        # Set transfer type
        status = self.ftp.transType('A')
        if not status:
            terminal.error('Transfer type set failed.')
            return False

        # Execute list command
        command = 'LIST'
        code, _ = self.ftp.sendCommand(command)
        if code != 150:
            return False

        # Read received data
        data = dataConn.read()
        showData = data.decode().strip()
        if len(showData) > 0:
            terminal.echo(showData)
        else:
            terminal.info("Empty directory.")
        status = self.ftp.read()
        if status.decode()[0:3] != 226:
            return False
        return True


class pwd:
    '''
        pwd
    '''

    ftp = None

    def __init__(self, ftp):
        '''
            init
        '''
        self.ftp = ftp

    def execute(self, cmd, params):
        '''
            execute
        '''
        command = 'PWD'
        code, message = self.ftp.sendCommand(command)
        if code != 257:
            terminal.error('PWD command execute failed: %d %s' %
                           (code, message))
            return False
        terminal.echo(message[message.find('"')+1:message.rfind('"')])
        return True


class cd:
    '''
        cd
    '''

    ftp = None

    def __init__(self, ftp):
        '''
            init
        '''
        self.ftp = ftp

    def execute(self, cmd, params):
        '''
            execute
        '''
        command = 'CWD %s' % params
        code, message = self.ftp.sendCommand(command)
        if code != 250:
            terminal.error('"cd %s" failed: %s' % (params, message))
            return False
        terminal.info(message)
        return True


# Register objects
base.regObj('ls', ls)
base.regObj('pwd', pwd)
base.regObj('cd', cd)
