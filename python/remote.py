#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import io
from . import terminal


class Connect:
    '''
        Connect
    '''

    BUFFER_SIZE = 4096
    host = ''
    port = ''
    user = ''
    password = ''
    conn = None

    def __init__(self):
        '''
            Init
        '''
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.close
        # ftpSock.setblocking(False)

    def connect(self, host, port):
        '''
            Connect
        '''
        self.host = host
        self.port = port
        try:
            self.conn.connect((self.host, self.port))
            return True
        except Exception as e:
            terminal.error('Connect data port failed: ' % str(e))
            return False

    def login(self):
        '''
            Login
        '''
        self.user = input('USER> ').strip()
        command = 'USER %s' % self.user
        code, message = self.send(command)
        if code != 331:
            terminal.error('%d %s' % (message))
            return False
        self.password = input('PASSWORD> ').strip()
        command = 'PASS %s' % self.password
        code, message = self.send(command)
        if code != 230:
            terminal.error('%d %s' % (code, message))
            return False
        terminal.info('Login success')
        return True

    def EPSV(self):
        '''
            Set EPSV
        '''
        code, message = self.send('EPSV')
        if code != 229:
            terminal.error('Set EPSV failed: %d %s' % (code, message))
            return False
        tmp = message[message.rfind('(')+1:message.rfind(')')].split('|')
        return int(tmp[3])

    def transType(self, mode):
        '''
            Set transfer type
        '''
        code, message = self.send('TYPE %s' % mode)
        if code != 200:
            terminal.error(message)
            return False
        return True

    def send(self, command):
        '''
            Send command to FTP server and return the result of execute.
        '''
        dataBytes = (command + '\r\n').encode()
        self.conn.sendall(dataBytes)
        result = self.read().decode()
        code = int(result[0:3])
        message = result[4:].strip()
        return code, message

    def read(self):
        '''
            Read all data from buffer
        '''
        data = b''
        while True:
            try:
                tmpData = self.conn.recv(self.BUFFER_SIZE)
                data = data + tmpData
                if len(tmpData) < self.BUFFER_SIZE:
                    break
            except EOFError:
                return
        return data
    
    def close(self):
        '''
            Connection close
        '''
        self.conn.close()
        terminal.info('Connection closed.')
    
    def __del__(self):
        '''
            Del
        '''
        self.close()
