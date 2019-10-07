#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import base
from .. import terminal


class qt:
    '''
        quit
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
        command = 'QUIT'
        code, message = self.ftp.sendCommand(command)
        if code != 221:
            terminal.error('Normal exit failure: %d %s' % (code, message))
        terminal.info('Goodbye.')
        exit()


# Register objects
base.regObj('quit', qt)
base.regObj('exit', qt)
