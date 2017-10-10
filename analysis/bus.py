import dateutil.parser
from   datetime import datetime
class bus:
    def __init__(self, busId):
        """Initializes a bus with a BusID"""
        #Min and max are the oldest and newest timestamps in the history
        self.busId   = busId
        self.history = []
        self.min     = None
        self.max     = None

    def _str2dt(self, str):
        """This method parses the timestamp into datetime object"""
        return dateutil.parser.parse(str)

    def logPoint(self, tsString, loc, busLine):
        """Adds a point to self.history

        tsString is a timestamp string from 511's XML file
        loc is a lat/lon tuple
        busLine is the busLine that the bus was operating as at that moment
        """

        ts = dateutil.parser.parse(tsString)
        self.history.append({"ts":ts, "loc":loc, "busLine":busLine})

        if((not self.min) or ts<self.min):
            self.min = ts

        if((not self.max) or ts>self.max):
            self.max = ts

    def getHistory(self, tsMin=None, tsMax=None):
        """Gets datapoints between two dates, all up to a date, or everything

        If two dates are specified, the program will output all datapoints
        between and including the two dates

        If only one date is specified, then the program will run as though
        the beginning date was unix epoch, and the end date the specified
        date and pull all datapoints between and including those dates

        If no parameter is specified it simply returns all history
        """

        #If both parameters are empty, just output entire history
        if tsMin == None and tsMax == None:
            return self.history

        #here we narrow out whether both tsMin and TsMax are defined,
        #or if only one.
        if tsMin and tsMax:
            tsMin = self._str2dt(tsMin)
            tsMax = self._str2dt(tsMax)

        elif tsMin and not tsMax:
            tsMax = self._str2dt(tsMin)
            tsMin = datetime(1970,1,1,0,0)

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

    def getNewestPoint(self, ts):
        """This function grabs the most recent datapoint as of a timestamp"""
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