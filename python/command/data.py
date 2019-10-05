#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from . import base
from .. import terminal, remote


class put:
    '''
        put
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
        status = self.ftp.transType('I')
        if not status:
            terminal.error('Transfer type set failed.')
            return False

        # Determine if the file exists
        if not os.path.exists(params):
            terminal.error('Local file no exist: %s' % params)
            return False

        # Read local file data
        fp = open(params, 'rb')
        data = fp.read()

        # Execute list command
        command = 'STOR %s' % params
        code, message = self.ftp.sendCommand(command)
        if code != 150:
            terminal.error(message)
            return False
        # Read received data
        status = dataConn.send(data)
        dataConn.close()
        if not status:
            return False
        code, message = self.ftp.readMessage()
        terminal.info('Data transfer success.')
        return True


class get:
    '''
        get
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
        status = self.ftp.transType('I')
        if not status:
            terminal.error('Transfer type set failed.')
            return False

        # Execute list command
        command = 'RETR %s' % params
        code, message = self.ftp.sendCommand(command)
        if code != 150:
            terminal.error('Exec command failed: %s' % message)
            return False

        # Read received data
        data = dataConn.read()
        fp = open(params, 'wb')
        status = fp.write(data)
        code, message = self.ftp.readMessage()
        if status < 0 or code != 226:
            terminal.error('File transfer failed: %s' % message)
            return False
        terminal.info(message)
        return True


class delete:
    '''
        delete
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

        # Execute list command
        command = 'DELE %s' % params
        code, message = self.ftp.sendCommand(command)
        if code != 250:
            terminal.error(message)
            return False
        terminal.info(message)
        return True


# Register objects
base.regObj('put', put)
base.regObj('get', get)
base.regObj('delete', delete)
