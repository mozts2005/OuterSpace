#
#  Copyright 2001 - 2007 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of Outer Space.
#
#  Outer Space is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Outer Space is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Outer Space; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import log
import datetime

class Scheduler(object):

	def __init__(self, gameMngr):
		self.gameMngr = gameMngr
		self.lastTick = self.getNow()
		self.tasks = []
		self.loadConfig()

	def tick(self):
		t = self.getNow()
		if t == self.lastTick:
			return
		log.debug("SCHEDULER", "Processing tick", t)
		for task in self.tasks:
			tmp = task.getNextEvent(t)
			log.debug("SCHEDULER", task.name, task.getNextEvent(t))
			if tmp == t:
				log.message("SCHEDULER",task.name, "Running action")
				try:
					task.callable()
				except Exception, e:
					log.warning("Cannot execute scheduler action")
		self.lastTick = t

	def getNow(self):
		return datetime.datetime.now().replace(second = 0, microsecond = 0)

	def loadConfig(self):
		# load cleanup
		self.loadTask(
			"CLEANUP", "scheduler:cleanup",
			self.gameMngr.clientMngr.cleanupSessions
		)
		# load turn processing
		self.loadTask(
			"TURN", "scheduler:turn",
			self.gameMngr.processTurnInternal
		)
		# load backup
		self.loadTask(
			"BACKUP", "scheduler:backup", 
			self.gameMngr.backupInternal
		)
		# load metaserver keepalive
		self.loadTask(
			"METAKEEPALIVE", "scheduler:metaserver",
			self.gameMngr.keepAlive
		)

	def loadTask(self, name, sectionName, action):
		for suffix in ("", ":0", ":1", ":2", ":3", ":4", ":5", ":6", ":7", ":8", ":9"):
			section = self.gameMngr.config.getSection(sectionName + suffix)
			enabled = section.enabled == "yes"
			if not enabled:
				continue
			minute = self.parse(section.minute)
			hour = self.parse(section.hour)
			day = self.parse(section.day)
			weekday = self.parse(section.weekday)
			month = self.parse(section.month)
			task = Task(minute = minute, hour = hour, weekday = weekday,
				day = day, month = month,
				callable = action,
				name = name + suffix
			)
			self.tasks.append(task)
	
	def parse(self, value):
		if value:
			return map(int, value.split(","))
		return []

class Task:

	def __init__(self, minute = [], hour = [], weekday = [], day = [], month = [], callable = None, name = None):
		assert not(weekday and day), "You cannot supply weekday and day at the same time"
		assert callable is not None, "You must supply a callable"
		self.doWeekday = bool(weekday)
		self.doDay = bool(day)
		self.minute = minute or range(0, 60)
		self.hour = hour or range(0, 24)
		self.weekday = weekday or range(0, 7)
		self.day = day or range(1, 32)
		self.month = month or range(1, 13)
		self.callable = callable
		self.name = name

	def __str__(self):
		compact = lambda s: ",".join(map(str, s))
		return "<%s %s %s-%s(%s) %s:%s>" % (
			self.__class__,
			self.name,
			compact(self.month), 
			compact(self.day),
			compact(self.weekday),
			compact(self.hour),
			compact(self.minute)
		)

	def getNumOfDaysInMonth(self, month, year):
		days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]
		if calendar.isleap(year) and month == 2:
			days += 1
		return days
	
	def getNextEvent(self, now):
		#@print "# CALLED", now
		event = now.replace(second = 0, microsecond = 0)
		# match a month
		found = False
		for i in self.month:
			if event.month < i:
				#@print "forced month", event,
				event = event.replace(month = i, day = 1, hour = 0, minute = 0)
				#@print "->", event
				found = True
				break
			elif event.month == i:
				#@print "perfect month", event
				found = True
				break
		if not found:
			#@print "next year", event,
			event = event.replace(year = event.year + 1, month = self.month[0], day = 1, hour = 0, minute = 0)
			#@print "->", event
		# match a day/weekday (only one of them can be specified)
		if self.doWeekday:
			found = False
			for i in self.weekday:
				if event.weekday() == i:
					#@print "perfect weekday", event
					found = True
					break
			if not found:
				#@print "next weekday", event, event.weekday(),
				event = event.replace(hour = 0, minute = 0) + datetime.timedelta(days = 1)
				#@print "->", event, event.weekday()
				return self.getNextEvent(event)
		elif self.doDay:
			found = False
			for i in self.day:
				if event.day < i:
					#@print "forced day", event,
					event = event.replace(day = i, hour = 0, minute = 0)
					#@print "->", event
					found = True
					break
				elif event.day == i:
					#@print "perfect day", event
					found = True
					break
			if not found:
				#@print "next month", event,
				event = event.replace(day = self.day[0], hour = 0, minute = 0) + datetime.timedelta(months = 1)
				#@print "->", event
				return self.getNextEvent(event)
		#  match an hour
		found = False
		for i in self.hour:
			if event.hour < i:
				#@print "forced hour", event,
				event = event.replace(hour = i, minute = 0)
				#@print "->", event
				found = True
				break
			if event.hour == i:
				#@print "perfect hour", event
				found = True
				break
		if not found:
			#@print "next day", event,
			event = event.replace(hour = self.hour[0], minute = 0) + datetime.timedelta(days = 1)
			#@print "->", event
			return self.getNextEvent(event)
		# match a minute
		found = False
		for i in self.minute:
			if event.minute <= i:
				#@print "forced minute", event,
				event = event.replace(minute = i)
				#@print "->", event
				found = True
				break
		if not found:
			#@print "next hour", event,
			event = event.replace(minute = self.minute[0]) + datetime.timedelta(hours = 1)
			#@print "->", event
			return self.getNextEvent(event)
		return event
	
if __name__ == "__main__":
	t = Task(minute = [5, 30], day = [10], month = [1], callable = log)
	print t.getNextEvent(datetime.datetime(2008, 11, 15, 23, 01))

	t = Task(minute = [1], hour = [0], day = [10], month = [1], callable = log)
	print t.getNextEvent(datetime.datetime(2008, 01, 10, 00, 02))

	t = Task(minute = [0, 30], weekday = [1,5], callable = log)
	print t.getNextEvent(datetime.datetime(2006, 11, 15, 22, 31))


