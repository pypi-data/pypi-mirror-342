import sys
import ctypes
class LEDArrayAnimationType:
	# Move the pattern in a positively incrementing direction
	ANIMATION_TYPE_FORWARD_SCROLL = 1
	# Move the pattern in a decrementing direction
	ANIMATION_TYPE_REVERSE_SCROLL = 2
	# Randomize LED RGB values based on the specified array
	ANIMATION_TYPE_POPCORN = 3
	# Flip the pattern and move it in a positively incrementing direction, starting from the animation end point
	ANIMATION_TYPE_FORWARD_SCROLL_MIRROR = 4
	# Flip the pattern and move it in a decrementing direction, starting from the animation end point
	ANIMATION_TYPE_REVERSE_SCROLL_MIRROR = 5

	@classmethod
	def getName(self, val):
		if val == self.ANIMATION_TYPE_FORWARD_SCROLL:
			return "ANIMATION_TYPE_FORWARD_SCROLL"
		if val == self.ANIMATION_TYPE_REVERSE_SCROLL:
			return "ANIMATION_TYPE_REVERSE_SCROLL"
		if val == self.ANIMATION_TYPE_POPCORN:
			return "ANIMATION_TYPE_POPCORN"
		if val == self.ANIMATION_TYPE_FORWARD_SCROLL_MIRROR:
			return "ANIMATION_TYPE_FORWARD_SCROLL_MIRROR"
		if val == self.ANIMATION_TYPE_REVERSE_SCROLL_MIRROR:
			return "ANIMATION_TYPE_REVERSE_SCROLL_MIRROR"
		return "<invalid enumeration value>"
