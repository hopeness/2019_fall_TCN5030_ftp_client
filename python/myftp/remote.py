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

    def connect(self, host, port):
        '''
            Connect
        '''
        self.host = host
        self.port = port
        try:
            self.conn.connect((self.host, self.port))
            self.conn.setblocking(True)
            return True
        except Exception as e:
            terminal.error('Connect data port failed: %s' % str(e))
            return False

    def terminalLogin(self):
        '''
            login by terminal
        '''
        self.user = input('USER> ').strip()
        self.password = input('PASSWORD> ').strip()
        return True

    def login(self, user=None, password=''):
        '''
            Login
        '''
        if user == None:
            user = self.user
            password = self.password
        command = 'USER %s' % user
        code, message = self.sendCommand(command)
        if code != 331:
            terminal.error('%d %s' % (code, message))
            return False
        command = 'PASS %s' % password
        code, message = self.sendCommand(command)
        if code != 230:
            terminal.error('%d %s' % (code, message))
            return False
        terminal.info('Login success')
        return True

    def EPSV(self):
        '''
            Set EPSV
        '''
        code, message = self.sendCommand('EPSV')
        if code != 229:
            terminal.error('Set EPSV failed: %d %s' % (code, message))
            return False
        tmp = message[message.rfind('(')+1:message.rfind(')')].split('|')
        return int(tmp[3])

    def transType(self, mode):
        '''
            Set transfer type
        '''
        code, message = self.sendCommand('TYPE %s' % mode)
        if code != 200:
            terminal.error(message)
            return False
        return True

    def sendCommand(self, command):
        '''
            Send command to FTP server and return the result of execute.
        '''
        dataBytes = (command + '\r\n').encode()
        self.send(dataBytes)
        return self.readMessage()

    def send(self, data):
        '''
            Send data to server.
        '''
        try:
            self.conn.sendall(data)
        except Exception as e:
            terminal.error('Send data to server failed: %s' % str(e))
            return False
        return True

    def readMessage(self):
        '''
            Read and format message to code and message
        '''
        result = self.read().decode()
        if len(result) == 0:
            return 0, 'Unknow error.'
        code = int(result[0:3])
        # Timeout re-connect
        if code == 421:
            terminal.error('FTP server connection timeout, please re-connect.')
            exit()
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
            except:
                break
        return data

    def close(self):
        '''
            Connection close
        '''
        self.conn.close()
        return True

    def __del__(self):
        '''
            Del
        '''
        self.close()
