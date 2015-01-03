#!/usr/bin/env python3

import datetime
import logging
import pytz
import time

from phue import Bridge

class LightProperties(object):
	brightness = None
	colorTemperature = None
	hue = None
	saturation = None

	def __init__(self):
		super(LightProperties, self).__init__()

	def getConfig(self):
		config = {}
		config['bri'] = self.brightness
		if (self.hue != None and self.saturation != None):
			config['hue'] = self.hue
			config['sat'] = self.saturation

		if (self.colorTemperature != None):
			config['ct'] = self.colorTemperature

		return config


class Schedule(object):
	lightProperties = {}
	localtz = pytz.timezone ("GMT")
	bridge = Bridge('huebridge', 'newdeveloper')
	lastEventTimeUsed = None

	def __init__(self):
		super(Schedule, self).__init__()
		self.bridge.connect()

		energize = LightProperties()
		energize.brightness = 237
		energize.colorTemperature = 155

		reading = LightProperties()
		reading.brightness = 240
		reading.colorTemperature = 343

		concentrate = LightProperties()
		concentrate.brightness = 219
		concentrate.colorTemperature = 234

		relax = LightProperties()
		relax.brightness = 144
		relax.colorTemperature = 467

		yellowSun = LightProperties()
		yellowSun.brightness = 150
		yellowSun.hue = 7826
		yellowSun.saturation = 250

		white = LightProperties()
		white.brightness = 220
		white.hue = 0
		white.saturation = 0

		orangeLow = LightProperties()
		orangeLow.brightness = 1
		orangeLow.hue = 2912
		orangeLow.saturation = 254

		self.lightProperties['energize'] = energize
		self.lightProperties['reading'] = reading
		self.lightProperties['concentrate'] = concentrate
		self.lightProperties['relax'] = relax
		self.lightProperties['yellowSun'] = yellowSun
		self.lightProperties['orangeLow'] = orangeLow
		self.lightProperties['white'] = white
		
	def setTimeZone(self, timezone):
		self.localtz = pytz.timezone(timezone)

	def registerLightSetting(self, name, setting):
		self.lightProperties[name] = setting

	def addEvent(self, hour, minute, second, name, settingName, transitionTimeInDeciseconds, lightOn = None):
		self.addGroupEvent(hour, minute, second, [name], settingName, transitionTimeInDeciseconds, lightOn)

	def addGroupEvent(self, hour, minute, second, names, settingName, transitionTimeInDeciseconds, lightOn = None):
		localTime = self.getLocalDateTime(hour, minute, second)
		config = self.getLightConfiguration(settingName, transitionTimeInDeciseconds, lightOn)
		logging.info(localTime.strftime("(%Y-%m-%d %H:%M:%S)") + " Adding event: " + settingName)
		logging.info("Lights: " + str(names))
		logging.debug("Configuration: " + str(config))
		for name in names:
			self.bridge.create_schedule(settingName, self.getUtcTimeString(localTime), self.bridge.get_light_id_by_name(name), config, settingName)
		self.lastEventTimeUsed = localTime

	def addEventByOffsetToLast(self, lastEventInDeciseconds, name, settingName, transitionTimeInDeciseconds, lightOn = None):
		self.addGroupEventByOffsetToLast(lastEventInDeciseconds, [name], settingName, transitionTimeInDeciseconds, lightOn)

	def addGroupEventByOffsetToLast(self, lastEventInDeciseconds, names, settingName, transitionTimeInDeciseconds, lightOn = None):
		if (self.lastEventTimeUsed != None):
			self.lastEventTimeUsed += datetime.timedelta(seconds = lastEventInDeciseconds / 10)
			self.addGroupEvent(self.lastEventTimeUsed.hour, self.lastEventTimeUsed.minute, self.lastEventTimeUsed.second, names, settingName, transitionTimeInDeciseconds, lightOn)
		else:
			logging.error("Error, called addEventByOffsetToLast without adding an initial event")

	def getLightConfiguration(self, settingName, transitionTimeInDeciseconds, lightOn):
		lightProperties = self.lightProperties[settingName]
		config = lightProperties.getConfig()
		if (lightOn != None):
			config['on'] = lightOn

		config['transitionTimeInDeciseconds'] = transitionTimeInDeciseconds

		return config

	def getUtcTimeString(self, dateTime):
		utcDateTime = dateTime.astimezone(pytz.utc)
		return utcDateTime.strftime("%Y-%m-%dT%H:%M:%S")

	def getLocalDateTime(self, hour, minute, second):
		localTime = datetime.datetime.now()
		localTime = localTime.replace(hour = hour, minute = minute, second = second)
		localTime = self.localtz.localize(localTime)#, is_dst=None)
		return localTime
