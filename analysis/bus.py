import dateutil.parser
class bus:
	def __init__(self, busId):
		#Min and max are the oldest and newest timestamps in the history
		self.busId   = busId
		self.history = []
		self.min     = None
		self.max     = None

	#This method parses the timestamp into datetime object
	def _str2dt(self, str):
		return dateutil.parser.parse(str)

	def logPoint(self, tsString, loc, busLine):
		#location is a lat/lon array
		ts = dateutil.parser.parse(tsString)
		self.history.append({"ts":ts, "loc":loc, "busLine":busLine})

		if((not self.min) or ts<self.min):
			self.min = ts

		if((not self.max) or ts>self.max):
			self.max = ts

	#this grabs datapoints between two TSs
	def getHistory(self, tsMin, tsMax):
		tsMin = self._str2dt(tsMin)
		tsMax = self._str2dt(tsMax)
		returnArr = []

		#This situation is nonsense and we won't have any of it
		if tsMax<tsMin:
			return None

		#discounting queries outside the known bounds of the log
		if tsMax<self.min or tsMin>self.max:
			return None

		if len(self.history) == 0:
			return None

		for point in self.history:
			if point["ts"]<tsMin:
				continue
			
			if point["ts"]>tsMax:
				break
			
			returnArr.append(point)

		if len(returnArr) == 0:
			return None
		else:
			return returnArr

	#this grabs the most recent datapoint as of a timestamp
	def getHistory(self, ts):
		returnArr = []

		#discounting queries outside the known bounds of the log
		if ts<self.min or ts>self.max:
			return None

		if len(self.history) == 0:
			return None

		target = 0
		for n, point in enumerate(self.history):
			if point["ts"]<ts:
				target = n
				continue
			
			if point["ts"]>ts:
				break
			
			return self.history[target]

	#this returns the entire history of a bus
	def getHistory(self):
		return self.history

