
import psycopg2
import random
import math

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
	listofGPSPoints[i] = {'latitude' : round(random.uniform(-90, 90), 4), 'longitude' : round(random.uniform(-180, 180), 4)}

try:
	for foo, bar in listofGPSPoints.items():
		print str(bar['latitude']) + ', ' + str(bar['longitude'])
		cur.execute("""INSERT INTO bostonunderwater_totem 
			(place, latitude, longitude, tier) 
			VALUES ('test node', {}, {}, 0)
			""".format(bar['latitude'], bar['longitude']))
		conn.commit()
except:
	print "something failed :("
