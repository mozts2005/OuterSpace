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

class ProgressBar(Widget):

	def __init__(self, parent, **kwargs):
		Widget.__init__(self, parent)
		# data
		self.min = 0
		self.max = 100
		self.value = 0
		# flags
		self.processKWArguments(kwargs)
		parent.registerWidget(self)

	def draw(self, surface):
		self.theme.drawProgressBar(surface, self)
		return self.rect

registerWidget(ProgressBar, 'progressbar')
