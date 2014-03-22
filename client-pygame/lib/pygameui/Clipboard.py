#
#  Copyright 2001 - 2007 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of Pygame.UI.
#
#  Pygame.UI is free software; you can redistribute it and/or modify
#  it under the terms of the Lesser GNU General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
#  Pygame.UI is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  Lesser GNU General Public License for more details.
#
#  You should have received a copy of the Lesser GNU General Public License
#  along with Pygame.UI; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import os

class Clipboard:
	"""Generic clipboard object. We have 2 working backends so far: Xsel
	and Windows. Xsel tends to break multibyte characters (not always),
	Windows Clipboard works fine."""

	def __init__(self):
		"""If no backend is available the Clipboard.clipboard variable is set to None,
		if running on Xsel it's set to int(1),
		if running on Windows it contains the clipboard_win module."""
		try:
			import Clipboard_win # we're on Windows
			self.clipboard = Clipboard_win
			del Clipboard_win
		except ImportError:
			if os.system("xsel &>/dev/null") == 0: # we're in X.org
				self.clipboard = 1
			else:
				self.clipboard = None # clipboard is N/A
	
	def read(self):
		"""Return a [] of unicode lines from the clipboard."""
		if self.clipboard == 1:
			pipe = os.popen("xsel -b -o", "rb")
			text = pipe.read()
			pipe.close()
			text = text.decode("utf-8")
		elif self.clipboard:
			text = self.clipboard.getText()
			text = text.decode("cp1250")
		
		return text.replace('\t', '   ').splitlines()
	
	def write(self, text):
		"""Receives a [] of unicode lines and writes them into the clipboard."""
		if self.clipboard == 1:
			text = '\n'.join(text)
			# encode from unicode to utf-8
			text = text.encode("utf-8")
			pipe = os.popen("xsel -b -i", "wb")
			pipe.write(text)
			pipe.close()
		elif self.clipboard:
			text = '\r\n'.join(text)
			# encode from unicode to cp1250
			try:
				text = text.encode("cp1250")
			except:
				text = text.encode("utf-8")
			self.clipboard.setText(text)
