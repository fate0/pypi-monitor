# -*- coding: utf-8 -*-

import os
import ssl
import json
import socket
import _socket
import distutils.spawn
import distutils.util
import distutils.ccompiler


logname = 'test'


def log(content):
    global logname
    with open('/tmp/%s.txt' % logname, 'ab') as fd:
        fd.write('%s\n' % json.dumps(content))


def fake_system(command):
    log({
        "func": "os.system",
        "params": [command]
    })
    if hasattr(os, 'system_'):
        return os.system_(command)


def fake_execv(path, args):
    log({
        "func": "os.execv",
        "params": [path, args]
    })
    if hasattr(os, 'execv_'):
        return os.execv_(path, args)


def fake_execve(path, args, env):
    log({
        "func": "os.execve",
        "params": [path, args]
    })
    if hasattr(os, 'execve_'):
        return os.execve_(path, args, env)


class FakeSSLSocket(ssl.SSLSocket):
    def __init__(self, *args, **kwargs):
        self.skip = False
        super(FakeSSLSocket, self).__init__(*args, **kwargs)

    def _real_connect(self, addr, connect_ex):
        if addr == ('1.1.1.1', 8080):
            self.skip = True

        return super(FakeSSLSocket, self)._real_connect(addr, connect_ex)

    def send(self, data, *args, **kwargs):
        if not self.skip:
            log({
                "func": "sslsocket.send",
                "params": [data]
            })

        return super(FakeSSLSocket, self).send(data, *args, **kwargs)

    def write(self, data):
        if not self.skip:
            log({
                "func": "sslsocket.write",
                "params": [data]
            })

        return super(FakeSSLSocket, self).write(data)


class FakeSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        self.skip = False
        super(FakeSocket, self).__init__(*args, **kwargs)

    def connect(self, address):
        if address == ('1.1.1.1', 8080):
            self.skip = True

        return super(FakeSocket, self).connect(address)

    def connect_ex(self, address):
        if address == ('1.1.1.1', 8080):
            self.skip = True

        return super(FakeSocket, self).connect_ex(address)

    def send(self, data, *args, **kwargs):
        if not self.skip:
            log({
                "func": "socket.send",
                "params": [data],
                "remote": self.getpeername()
            })

        return super(FakeSocket, self).send(data, *args, **kwargs)

    def sendall(self, data, *args, **kwargs):
        if not self.skip:
            log({
                "func": "socket.sendall",
                "params": [data],
                "remote": self.getpeername()
            })

        return super(FakeSocket, self).sendall(data, *args, **kwargs)

    def sendto(self, data, *args, **kwargs):
        if not self.skip:
            log({
                "func": "socket.sendto",
                "params": [data, args, kwargs],
            })

        return super(FakeSocket, self).sendto(data, *args, **kwargs)


def fake_spawn(*args, **kwargs):
    global logname
    try:
        unpatch()
        distutils.spawn.spawn_(*args, **kwargs)
    finally:
        patch(logname)


def patch(name):
    global logname
    logname = name

    if not hasattr(os, 'system_'):
        os.system_ = os.system
        os.system = fake_system

    if not hasattr(os, 'execv_'):
        os.execv_ = os.execv
        os.execv = fake_execv

    if not hasattr(os, 'execve_'):
        os.execve_ = os.execve
        os.execve = fake_execve

    if not hasattr(ssl, 'SSLSocket_'):
        ssl.SSLSocket_ = ssl.SSLSocket
        ssl.SSLSocket = FakeSSLSocket

    if not hasattr(socket, 'socket_'):
        socket.socket_ = socket.socket
        socket.socket = socket.SocketType = socket._socketobject = FakeSocket

    if not hasattr(_socket, 'socket_'):
        _socket.socket_ = _socket.socket
        _socket.socket = _socket.SocketType = FakeSocket

    if not hasattr(distutils.spawn, 'spawn_'):
        distutils.spawn.spawn_ = distutils.spawn.spawn
        distutils.spawn.spawn = fake_spawn
        distutils.util.spawn = fake_spawn
        distutils.ccompiler.spawn = fake_spawn


def unpatch():
    if hasattr(os, 'system_'):
        os.system = os.system_

    if hasattr(os, 'execv_'):
        os.execv = os.execv_

    if hasattr(os, 'execve_'):
        os.execve = os.execve_

    if hasattr(ssl, 'SSLSocket_'):
        ssl.SSLSocket = ssl.SSLSocket_

    if hasattr(socket, 'socket_'):
        socket.socket = socket.SocketType = socket._socketobject = socket.socket_

    if hasattr(_socket, 'socket_'):
        _socket.socket = _socket.SocketType = _socket.socket_

    if hasattr(distutils.spawn, 'spawn_'):
        distutils.spawn.spawn = distutils.spawn.spawn_
        distutils.util.spawn = distutils.spawn.spawn_
        distutils.ccompiler.spawn = distutils.spawn.spawn_
