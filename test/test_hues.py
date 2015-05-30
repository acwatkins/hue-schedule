#!/usr/bin/env python3

import datetime
import hues
import pytest
import pytz

@pytest.mark.parametrize("seed", [3, 23])
def test_getConfig(seed):
	lightProperties = hues.LightProperties()
	lightProperties.brightness = 132 + seed
	lightProperties.colorTemperature = 245 + seed
	lightProperties.hue = 23483 + seed
	lightProperties.saturation = 32 + seed

	assert lightProperties.getConfig() == { 'bri': lightProperties.brightness, 'ct': lightProperties.colorTemperature, \
		'hue': lightProperties.hue, 'sat': lightProperties.saturation }

@pytest.mark.parametrize("seed", [0, 7, 31])
def test_lightPropertyBounds(seed):
	lightProperties = hues.LightProperties()
	lightProperties.brightness = 255
	lightProperties.brightness = 128 + seed
	lightProperties.brightness = 0
	with pytest.raises(ValueError):
		lightProperties.brightness = 256 + seed
	with pytest.raises(ValueError):
		lightProperties.brightness = -1 - seed

@pytest.mark.parametrize("seed", [0, 5, 17])
def test_colorTemperatureBounds(seed):
	lightProperties = hues.LightProperties()
	lightProperties.colorTemperature = 500
	lightProperties.colorTemperature = 255 + seed
	lightProperties.colorTemperature = 153
	with pytest.raises(ValueError):
		lightProperties.colorTemperature = 501 + seed
	with pytest.raises(ValueError):
		lightProperties.colorTemperature = 152 - seed

@pytest.mark.parametrize("seed", [0, 3, 23])
def test_hueBounds(seed):
	lightProperties = hues.LightProperties()
	lightProperties.hue = 0
	lightProperties.hue = 32000 + seed
	lightProperties.hue = 65535
	with pytest.raises(ValueError):
		lightProperties.hue = -1 - seed
	with pytest.raises(ValueError):
		lightProperties.hue = 65536 + seed

@pytest.mark.parametrize("seed", [0, 3, 23])
def test_saturation(seed):
	lightProperties = hues.LightProperties()
	lightProperties.saturation = 0
	lightProperties.saturation = 128 + seed
	lightProperties.saturation = 255
	with pytest.raises(ValueError):
		lightProperties.saturation = -1 - seed
	with pytest.raises(ValueError):
		lightProperties.saturation = 256 + seed

@pytest.mark.parametrize("year, month, day, hour, minute, second", [(2012, 3, 17, 18, 1, 2), (2013, 3, 9, 1, 30, 31)])
def test_localDateTime(year, month, day, hour, minute, second):
	timezone = pytz.timezone("America/New_York")
	hues.setTimezone(timezone)
	localDateTime = hues.LocalDateTime(hour, minute, second, datetime.date(year, month, day))
	expectedDateTime = datetime.datetime(year, month, day, hour, minute, second)
	expectedDateTime = timezone.localize(expectedDateTime)
	assert localDateTime == expectedDateTime
