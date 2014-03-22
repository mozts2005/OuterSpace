#
#  Copyright 2001 - 2006 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of IGE - Outer Space.
#
#  IGE - Outer Space is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  IGE - Outer Space is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with IGE - Outer Space; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import os
from ige.ospace.Const import *
from ige.IDataHolder import makeIDataHolder
from ige import log

rulesetName = None
rulesetPath = None

def initRules(path):
	log.message("Using ruleset", path)
	# import rules
	import sys
	try:
		importFromPath(path)
	except ImportError:
		path = os.path.join("../server/res/rules", os.path.basename(path))
		importFromPath(path)
	# import technologies
	import Techs
	global techs, Tech
	techs, Tech = Techs.initTechnologies(path)
	global rulesetName, rulesetPath
	rulesetName = os.path.basename(path)
	rulesetPath = path

def importFromPath(path):
	import sys
	oldpath = sys.path
	try:
		sys.path = [path]
		log.debug("Rules import - using path", sys.path)
		exec "from rules import *" in globals()
		log.message("Rules import succeeded")
	finally:
		sys.path = oldpath
	
