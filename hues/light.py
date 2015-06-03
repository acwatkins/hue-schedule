#!/usr/bin/env python3

class LightProperties(object):
	_brightness = None
	_colorTemperature = None
	_hue = None
	_saturation = None

	def __init__(self):
		super(LightProperties, self).__init__()

	@property
	def brightness(self):
		return self._brightness

	@brightness.setter
	def brightness(self, value):
		if value > 255:
			raise ValueError("Brightness value above 255 is not possible")
		if value < 0:
			raise ValueError("Brightness value below -1 is not possible")
		self._brightness = value

	@property
	def colorTemperature(self):
		return self._colorTemperature

	@colorTemperature.setter
	def colorTemperature(self, value):
		if value > 500:
			raise ValueError("colorTemperature value above 500 is not possible")
		if value < 153:
			raise ValueError("colorTemperature value below 153 is not possible")
		self._colorTemperature = value

	@property
	def hue(self):
		return self._hue

	@hue.setter
	def hue(self, value):
		if value > 65535:
			raise ValueError("Hue value above 65535 is not possible")
		if value < 0:
			raise ValueError("Hue value below 0 is not possible")
		self._hue = value

	@property
	def saturation(self):
		return self._saturation

	@saturation.setter
	def saturation(self, value):
		if value > 255:
			raise ValueError("Saturation value above 255 is not possible")
		if value < 0:
			raise ValueError("Saturation value below 0 is not possible")
		self._saturation = value

	def getConfig(self):
		config = {}
		config['bri'] = self.brightness
		if (self.hue != None and self.saturation != None):
			config['hue'] = self.hue
			config['sat'] = self.saturation

		if (self.colorTemperature != None):
			config['ct'] = self.colorTemperature

		return config
