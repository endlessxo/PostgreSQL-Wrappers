'''
This python script inserts a test totem in the database called Childrens Museum of
latitude 42.3393 and longitude -71.1012 with tier 0.
'''
import psycopg2


try:
        conn = psycopg2.connect("dbname='django' user='django' host='localhost' password='EBmpfDB8NN'")
except:
        print "I am unable to connect to the database"

cur = conn.cursor()

try:
	cur.execute("""
		INSERT INTO bostonunderwater_totem 
		(place, latitude, longitude, tier) 
		VALUES 
		('Childrens Museum', 42.3393, -71.1012, 0)
	""")
	conn.commit()

except:
	print "the insert failed :("
try: 
	cur.execute("""
		SELECT * FROM bostonunderwater_totem WHERE tier >= 0
	""")

except:
	print "the query failed."

rows = cur.fetchall()
dict = {}


print "\n Show me the databases: \n"

for row in rows:
        dict[row[1]] = {'node number' : row[0], 'name' : row[1], 'latitude' : row[2], 'longitude' : row[3]}

for i in dict:
	print i

