#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .. import terminal
from . import base


class help:
    '''
        help
    '''

    command = b''

    def __init__(self, ftp):
        '''
            init
        '''
        pass

    def execute(self, cmd, params):
        '''
            execute
        '''
        info = r'''Supported CMD:
    ls list
    cd remote-dir
    get remote-file
    put local-file
    delete remote-file
    quit/exit
    help/?'''
        terminal.echo(info)
        return True


# Register object
base.regObj('help', help)
base.regObj('?', help)
