#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from . import terminal


def run():
    '''
        Program init function
    '''
    cmd = param = ''
    statement = input('FTP> ').strip()
    spIdx = statement.find(' ')
    if statement == '':
        # If standard input is empty
        return None
    elif spIdx < 0:
        # If the input has no space
        cmd = statement
    else:
        # Else situation has command and parameters
        cmd = statement[0:spIdx]
        param = statement[spIdx+1:]
    return cmd, param


def echo(msg):
    '''
        Print message
    '''
    print(msg)

def info(msg):
    '''
        Print message with infomation
    '''
    print('[%s] %s' % (formatTime(), msg))

def error(msg):
    '''
        Print error message
    '''
    print('[%s] Error: %s' % (formatTime(), msg))


def formatTime():
    '''
        Format time
    '''
    return time.strftime('%H:%M:%S', time.localtime())
