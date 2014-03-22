#
#  Copyright 2001 - 2006 Ludek Smid [http://www.ospace.net/]
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

from pygame.locals import *
from Const import *
from Widget import Widget, registerWidget

class Check(Widget):

	def __init__(self, parent, **kwargs):
		Widget.__init__(self, parent)
		# data
		self.__dict__['text'] = None
		self.__dict__['icons'] = []
		# flags
		self.__dict__['action'] = None
		self.__dict__['rmbAction'] = None
		self.__dict__['checked'] = 0
		self.__dict__['_processingMB1'] = 0
		self.__dict__['_processingMB3'] = 0
		self.align = ALIGN_W
		self.processKWArguments(kwargs)
		parent.registerWidget(self)

	def draw(self, surface):
		self.theme.drawCheck(surface, self)
		return self.rect

	def processMB1Down(self, evt):
		self.checked = not self.checked
		self._processingMB1 = 1
		return NoEvent

	def processMB1Up(self, evt):
		self.processAction(self.action)
		self._processingMB1 = 0
		return NoEvent

	def processMB1UpMissed(self, evt):
		self._processingMB1 = 0
		return Widget.processMB1UpMissed(self, evt)

	def onMouseOut(self):
		if self._processingMB1:
			self.checked = not self.checked
		return Widget.onMouseOut(self)

	def onMouseOver(self):
		if self._processingMB1:
			self.checked = not self.checked
		return Widget.onMouseOver(self)

	def onFocusLost(self):
		self._processingMB1 = 0
		self._processingMB3 = 0
		return Widget.onFocusLost(self)

	def processMB3Down(self, evt):
		self._processingMB3 = 1
		return NoEvent

	def processMB3Up(self, evt):
		if self._processingMB3:
			self.processAction(self.rmbAction)
		self._processingMB3 = 0
		return NoEvent

registerWidget(Check, 'check')
