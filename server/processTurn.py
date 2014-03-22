#!/usr/bin/env python2.2

# tweak PYTHONPATH
import sys
sys.path.insert(0, 'lib')

from igeclient.IClient import IClient
import time

def msgHandler(id, data):
	if id >= 0:
		print 'Message', id, data

#s = IClient('ige.qgir.cz:9080', None, msgHandler, 'IClient/osc')
#s = IClient('212.11.104.99:9080', None, msgHandler, None, 'IClient/osc')
s = IClient('127.0.0.1:9080', None, msgHandler, None, 'IClient/osc')

login = "admin"
password = "WhateverYourPasswordIs"

s.connect(login)
s.login('Alpha', login, password)

s.processTurn()

s.logout()
