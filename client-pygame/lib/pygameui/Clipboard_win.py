# -*- Mode: Python; tab-width: 4 -*-
#	Author: Wesley Phoa <doctorwes@mindspring.com>
#

"""\
Read from and write to the Windows clipboard.
Interprets clipboard data either as text or an array of data.
Can be used in two different ways depending on taste:

	(a)	import clipboard
		clipboard.setText("hello")
		dat = clipboard.getData() # returns list-of-lists

	(b)	from clipboard import theclipboard
		theclipboard.data = [[5,6.4], [7,8], [0.5,12]]
		txt = theclipboard.text
		theclipboard.array # returns 2D NumPy array

Requires:	Sam Rushing's calldll module
References:	MS Support site article IDs: Q138909, Q138910
Warnings:	Minimal error checking in this version!

Copyright (C) 1999, Wesley Phoa; distributed under the GPL.
Version 0.01, 06/08/1999 - any comments greatly appreciated!
        0.02, 06/08/1999 - some support for NumPy arrays
		0.03, 06/10/1999 - bug fixes: float convert, padding
"""

import types, string
from dynwin import calldll, windll
try:
	import Numeric
except:
	pass

# constants from win32con
CF_TEXT = 1
GHND = 66

user32 = windll.module('User32')
kernel32 = windll.module('Kernel32')

def fl(s):
	if s == '':
		return 0
	else:
		return float(s)

def getText():
	"""\
Get string from clipboard (CF_TEXT format)
	"""
	if user32.OpenClipboard(0):
		hClipMemory = user32.GetClipboardData(CF_TEXT)
		lpClipMemory = kernel32.GlobalLock(hClipMemory)
		text = calldll.read_string(lpClipMemory)
		kernel32.GlobalUnlock(hClipMemory)
		user32.CloseClipboard()
		return text
	else:
		return ''

def setText(text):
	"""\
Place string onto clipboard (CF_TEXT format)
	"""
	text = windll.cstring(text)
	hGlobalMemory = kernel32.GlobalAlloc(GHND, len(text)+1)
	lpGlobalMemory = kernel32.GlobalLock(hGlobalMemory)
	lpGlobalMemory = kernel32.lstrcpy(lpGlobalMemory, text)
	kernel32.GlobalUnlock(hGlobalMemory)
	if user32.OpenClipboard(0):
		user32.EmptyClipboard()
		user32.SetClipboardData(CF_TEXT, hGlobalMemory)
		user32.CloseClipboard()

def makelist(val):
	if type(val)<>types.ListType:
		return [val]
	else:
		return val

def getData(numerical=1):
	"""\
Assume clipboard data is delimited by TAB, CR/LF; e.g. copied from Excel
Return list-of-lists; if argument=1, try to convert elements to floats
	"""
	text = getText()
	try:
		data = map(lambda s: string.split(s, '\011'), string.split(text, '\015\012'))
		while data[-1] == ['']:
			data = data[0:-1]
		if numerical:
			data = map(lambda list: map(fl, list), data)
			maxlen = max(map(len,data))
			for i in range(0, len(data)):
				data[i] = data[i] + (maxlen - len(data[i]))*[0]
		return data
	except TypeError:
		return [[]]
	except IndexError:
		return [[]]

def setData(data):
	"""\
Given list-of-lists, convert to string delimited by TAB, CR/LF
Put on clipboard; can now (e.g.) be pasted into an Excel range
	"""
	data = makelist(data)
	data = map(makelist, data)
	data = map(lambda list: map(str, list), data)
	text = string.join(map(lambda list: string.join(list, '\011'), data), '\015\012')
	setText(text)

class ClipboardAccess:
	"""\
Windows clipboard access via object with text and data attributes,
where text attribute is a string and data attribute is a list-of-lists.
	"""

	def __getattr__(self, name):
		if name == 'text':
			return getText()
		elif name == 'data':
			try:
				return getData(1)	# try to return floats if possible
			except ValueError:
				return getData(0)
		elif name == 'array':
			try:
				return Numeric.array(self.data)
			except:
				return self.data
		else:
			raise AttributeError, "ClipboardAccess has no attribute '" + name + "'"

	def __setattr__(self, name, val):
		if name == 'text':
			setText(val)
		elif name == 'data':
			setData(val)
		elif name == 'array':
			try:
				setData(val.tolist())
			except:
				setData(val)
		else:
			raise AttributeError, "ClipboardAccess has no attribute '" + name + "'"

theclipboard = ClipboardAccess()

if __name__ == '__main__':
	print 'Clipboard text: '
	print getText()
	setText("spam!")
