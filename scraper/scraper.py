#This is a very bare scraper. In intervals on a single thread,
#it dumps the currently running busses at AC transit into a database.
#The routine to prevent duplicate entries is very inefficient but I have chosen
#To focus my attention on the visual analysis of the busses.

import sqlite3
import urllib.request
import time
import json


con = sqlite3.connect("./database.db")
cur = con.cursor()
apiKey = "api key here"

cur.execute("CREATE TABLE IF NOT EXISTS busList (id INTEGER PRIMARY KEY, "+
	"BusId INTEGER, busLine VARCHAR(10), RecordedAtTime TEXT, "+
	"latitude NUMERIC, longitude NUMERIC);")

busListAddr = "http://api.511.org/transit/vehiclemonitoring?agency=actransit"+
	"&api_key="+apiKey

while True:
	busListRaw = urllib.request.urlopen(busListAddr).read().decode()[1:]
	data = json.loads(busListRaw)
	busList = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]
	for bus in busList:
		busInfo=bus["MonitoredVehicleJourney"]

		#check if entry already exists
		cur.execute("SELECT id FROM busList WHERE busId == ? AND RecordedAtTime == ?",(busInfo["VehicleRef"],bus["RecordedAtTime"]))
		check = cur.fetchone()

		if check == None:
			cur.execute("insert into busList(busId, busLine, RecordedAtTime, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
				(busInfo["VehicleRef"], busInfo["LineRef"],bus["RecordedAtTime"],busInfo["VehicleLocation"]["Latitude"],busInfo["VehicleLocation"]["Longitude"]))
		else:
			continue

	con.commit()
	time.sleep(60)