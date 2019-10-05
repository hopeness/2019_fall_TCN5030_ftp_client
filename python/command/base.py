#!/usr/bin/env python
# -*- coding:utf-8 -*-

__commandMap = {}
__serverStatus = False


def setConnStatus(status):
    '''
        test
    '''
    __serverStatus = status


def getConnStatus():
    '''
        test
    '''
    return __serverStatus


def regObj(name, obj):
    '''
        test
    '''
    if name not in __commandMap:
        __commandMap[name] = obj
    return True


def getObj(name):
    '''
        test
    '''
    if name in __commandMap:
        return __commandMap[name]
    return None
