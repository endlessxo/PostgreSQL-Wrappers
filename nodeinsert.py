
import psycopg2
import random
import math
from datetime import datetime

#Latitudes go from -90 to 90
#Longitude go from -180 to 180
numofDataPoints = 14
listofGPSPoints = {}

try:
        conn = psycopg2.connect("dbname='django' user='django' host='localhost' password='EBmpfDB8NN'")
except:
        print "I am unable to connect to the database"
cur = conn.cursor()

for i in range (0, numofDataPoints):
	listofGPSPoints[i] = {'latitude' : round(random.uniform(-90, 90), 4), 'longitude' : round(random.uniform(-180, 180), 4), 'water_level' : random.randint(0, 3), 'node_number' : i}

print str(datetime.now())	

try:
	
	for foo, bar in listofGPSPoints.items():

		cur.execute("""INSERT INTO bostonunderwater_node 
		(latitude, longitude, water_level, node_number, time)
		VALUES ({}, {}, {}, {}, '2015/02/07 16:51.01')
		""".format(bar['latitude'], bar['longitude'], bar['water_level'], bar['node_number']))

#		cur.execute("""INSERT INTO bostonunderwater_node
#               (latitude, longitude, water_level, node_number, time)
#               VALUES ({}, {}, {}, {}, {})
#               """.format(bar['latitude'], bar['longitude'], bar['water_level'], bar['node_number'], str(datetime.now())))
		
		conn.commit()
except:
	print "something failed :("
