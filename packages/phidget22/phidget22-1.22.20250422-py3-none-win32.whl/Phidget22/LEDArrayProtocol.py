import sys
import ctypes
class LEDArrayProtocol:
	# Byte order RGB (WS2811)
	LED_PROTOCOL_RGB = 1
	# Byte order GRB (WS2812B, SK6812)
	LED_PROTOCOL_GRB = 2
	# Byte order RGBW
	LED_PROTOCOL_RGBW = 3
	# Byte order GRBW (SK6812RGBW)
	LED_PROTOCOL_GRBW = 4

	@classmethod
	def getName(self, val):
		if val == self.LED_PROTOCOL_RGB:
			return "LED_PROTOCOL_RGB"
		if val == self.LED_PROTOCOL_GRB:
			return "LED_PROTOCOL_GRB"
		if val == self.LED_PROTOCOL_RGBW:
			return "LED_PROTOCOL_RGBW"
		if val == self.LED_PROTOCOL_GRBW:
			return "LED_PROTOCOL_GRBW"
		return "<invalid enumeration value>"
