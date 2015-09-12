#!/usr/bin/env python3

import collections
import datetime
import hues.light
import logging
import pytz

from phue import Bridge

timezone = None

def setTimezone(tz):
	global timezone
	timezone = tz

class LocalDateTime(datetime.datetime):
	def __new__(self, hour, minute, second, date=None):
		if date is None:
			date = datetime.datetime.today()
		localDateTime = super(LocalDateTime, self).__new__(self, date.year, date.month, date.day, hour, minute, second)
		localDateTime = timezone.localize(localDateTime)
		return localDateTime

class Schedule(object):
	def __init__(self, bridgeIp, bridgeUser):
		super(Schedule, self).__init__()
		self.bridge = Bridge(bridgeIp, bridgeUser)
		self.bridge.connect()

		energize = hues.light.LightProperties()
		energize.brightness = 237
		energize.colorTemperature = 155

		reading = hues.light.LightProperties()
		reading.brightness = 240
		reading.colorTemperature = 343

		concentrate = hues.light.LightProperties()
		concentrate.brightness = 219
		concentrate.colorTemperature = 234

		relax = hues.light.LightProperties()
		relax.brightness = 144
		relax.colorTemperature = 467

		yellowSun = hues.light.LightProperties()
		yellowSun.brightness = 125
		yellowSun.hue = 7826
		yellowSun.saturation = 250

		white = hues.light.LightProperties()
		white.brightness = 220
		white.hue = 0
		white.saturation = 0

		orangeLow = hues.light.LightProperties()
		orangeLow.brightness = 75
		orangeLow.hue = 2912
		orangeLow.saturation = 254

		redLowest = hues.light.LightProperties()
		redLowest.brightness = 0
		redLowest.hue = 0
		redLowest.saturation = 254

		self.lightProperties = {}
		self.lightProperties['energize'] = energize
		self.lightProperties['reading'] = reading
		self.lightProperties['concentrate'] = concentrate
		self.lightProperties['relax'] = relax
		self.lightProperties['yellowSun'] = yellowSun
		self.lightProperties['orangeLow'] = orangeLow
		self.lightProperties['redLowest'] = redLowest
		self.lightProperties['white'] = white
		
		self.lastEventTimeUsed = None

	def registerLightSetting(self, name, setting):
		self.lightProperties[name] = setting

	def addEvent(self, beginDateTime, names, settingNames, transitionTimeInDeciseconds = None, endDateTime = None, lightOn = None):
		if isinstance(names, str):
			names = [names]
		if isinstance(settingNames, str):
			settingNames = [settingNames]

		if (transitionTimeInDeciseconds == None and endDateTime == None):
			logging.error("addEvent: Must either specify transition time or end date time")
			return
		logging.info("------------------------------------------------------------------")
		eventDateTime = beginDateTime
		logging.info(eventDateTime.strftime("(%Y-%m-%d %H:%M:%S)") + " Adding event: " + str(settingNames))
		logging.info("Lights: " + str(names))

		durationBetweenEventsInDeciseconds = transitionTimeInDeciseconds
		if (endDateTime != None):
			deltaDateTime = endDateTime - beginDateTime
			deltaDateTimeInSeconds = deltaDateTime / datetime.timedelta(seconds = 1)

			secondsPerTransition = int(deltaDateTimeInSeconds / len(settingNames))
			durationBetweenEventsInDeciseconds = secondsPerTransition * 10
			transitionTimeInDeciseconds = (secondsPerTransition - 1) * 10

			logging.info("deltaTime: " + str(deltaDateTime))
			logging.info("minutesPerTransition: " + str(secondsPerTransition / 60))
		elif (transitionTimeInDeciseconds != None and len(settingNames) > 1):
			durationBetweenEventsInDeciseconds /= len(settingNames)
			transitionTimeInDeciseconds = durationBetweenEventsInDeciseconds - 10

		for settingName in settingNames:
			for name in names:
				config = self.getLightConfiguration(settingName, transitionTimeInDeciseconds, lightOn)
				self.bridge.create_schedule(settingName, self.getUtcTimeString(eventDateTime), self.bridge.get_light_id_by_name(name), config, settingName)
			eventDateTime += datetime.timedelta(seconds=durationBetweenEventsInDeciseconds / 10)
		self.lastEventTimeUsed = eventDateTime

	def addEventByOffsetToLast(self, lastEventInDeciseconds, names, settingName, transitionTimeInDeciseconds, lightOn = None):
		if self.lastEventTimeUsed is not None:
			self.lastEventTimeUsed += datetime.timedelta(seconds=lastEventInDeciseconds / 10)
			self.addEvent(self.lastEventTimeUsed, names, settingName, transitionTimeInDeciseconds, lightOn)
		else:
			logging.error("Error, called addEventByOffsetToLast without adding an initial event")

	def getLightConfiguration(self, settingName, transitionTimeInDeciseconds, lightOn):
		lightProperties = self.lightProperties[settingName]
		config = lightProperties.getConfig()
		if lightOn is not None:
			config['on'] = lightOn

		config['transitiontime'] = transitionTimeInDeciseconds

		return config

	def getUtcTimeString(self, dateTime):
		utcDateTime = dateTime.astimezone(pytz.utc)
		return utcDateTime.strftime("%Y-%m-%dT%H:%M:%S")
