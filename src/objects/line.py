from .point import Point


class Line:
	"""A line consists of two points in space"""
	def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
		self.point_start = Point(x1, y1, z1)
		self.point_end = Point(x2, y2, z2)
