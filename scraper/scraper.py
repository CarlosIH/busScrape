#This is a very bare scraper. In intervals on a single thread,
#it dumps the currently running busses at AC transit into a database.

import sqlite3
import urllib.request
import time
import json

con = sqlite3.connect("../database.db")
apiKey = "api key here"

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS busList (id INTEGER PRIMARY KEY, "
    "BusId INTEGER, busLine VARCHAR(10), RecordedAtTime TEXT, "
    "latitude NUMERIC, longitude NUMERIC);")

busListAddr = ("http://api.511.org/transit/vehiclemonitoring?agency=actransit"
    "&api_key="+apiKey)

#This dict stores the most recent TS of a bus
busAge = {}

#Initialize with the age of all busses currently in the database
cur.execute("SELECT BusID, RecordedAtTime FROM busList GROUP BY BusID "
    "ORDER BY RecordedAtTime ASC;")
check = cur.fetchall()
for bus in check:
    busAge[bus[0]] = bus[1]

while True:
    busListRaw = urllib.request.urlopen(busListAddr).read().decode()[1:]
    data = json.loads(busListRaw)["Siri"]["ServiceDelivery"]
    busList = data["VehicleMonitoringDelivery"]["VehicleActivity"]
    for bus in busList:
        busInfo = bus["MonitoredVehicleJourney"]

        if busInfo["VehicleRef"] not in busAge or \
            busAge[busInfo["VehicleRef"]] is not bus["RecordedAtTime"]:

            cur.execute("insert into busList(busId, busLine,"
                "RecordedAtTime, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                (busInfo["VehicleRef"], busInfo["LineRef"],
                bus["RecordedAtTime"],busInfo["VehicleLocation"]["Latitude"],
                busInfo["VehicleLocation"]["Longitude"]))
            busAge[busInfo["VehicleRef"]] = bus["RecordedAtTime"]
        else:
            continue

    con.commit()
    time.sleep(60)