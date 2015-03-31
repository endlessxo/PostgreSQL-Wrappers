'''
This script connects to the database and runs a simple select from where query in 
postgresql!
It then encodes this information into geoJSON objects and outputs a geoJSON file
'''
import psycopg2
import geojson
from geojson import Point, Feature, FeatureCollection
	
try:
	conn = psycopg2.connect("dbname='django' user='django' host='localhost' password='EBmpfDB8NN'")
except:
	print "I am unable to connect to the database"

cur = conn.cursor()
cur.execute("""	
	SELECT * from bostonunderwater_node WHERE water_level >= '0'
""")


rows = cur.fetchall()
dict = {}

#DATABASE FORMAT
#ROW 0 = node_number
#ROW 1 = latitude
#ROW 2 = longitude
#ROW 3 = time
#ROW 4 = water_level

print "\n Show me the databases: \n"
for row in rows:
       	dict[row[0]] = {'latitude' : str(row[1]), 'longitude' : str(row[2]), 'time' : str(row[3]), 'water_level' : str(row[4]), 'node_number' : str(row[0])}

print dict

nodeCount = 0
plist=[]
flist=[]
for node in dict:
        #Cast our GPS coords into floats
        lat =  float(dict[node]['latitude'])
        lon = float(dict[node]['longitude'])
        print "\n Point = %d : Lat = %f Long = %f" % (nodeCount,lat,lon)
        
        #Increase nodeCount
        nodeCount += 1

        # Generate point and add to point list
        point = Point((lon,lat))
        plist.append(point)

        # Generate feature w/ properties and add it to feature list
        feature = Feature(geometry=point, properties={"nodeNumber": dict[node]['node_number'], "waterLevel": dict[node]['water_level'], "time": dict[node]['time'], "longitude": dict[node]['longitude'], "latitude": dict[node]['latitude']}, id=str(nodeCount))
        flist.append(feature)

# Generate Feature Collection and dump to file
FeatureClct = FeatureCollection(flist)

#Encode FeatureCollection as JSON
dump = geojson.dumps(FeatureClct, sort_keys=True)
print dump
with open("output.json", "w") as text_file:
        text_file.write("%s" % dump)
