#Let me walk you through this code.
#Import the PostgreSQL stuff
import psycopg2


try:
#Then we try to connect to the database with the credentials below. It is displayed when you $
        conn = psycopg2.connect("dbname='django' user='django' host='localhost' password='EBmpfDB8NN'")
except:
#The bottom line should never happen because we have the correct credentials.
        print "I am unable to connect to the database"

#We connect the cursor
cur = conn.cursor()

The bottom line is the workhorse of this code. This is where the magic happens folks.
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


#Now we run the query to populate the dictionary with the totems
try: 
	cur.execute("""
		SELECT * FROM bostonunderwater_totem WHERE tier >= 0
	""")

except:
	print "the query failed."

rows = cur.fetchall()

#A new dictionary is created to display the data in a coherant way.
dict = {}


print "\n Show me the databases: \n"
for row in rows:
#for each row of the bostonunderwater_totem, make a hash table that can be addressed by the name.
#The name can be attained by row[1] fyi.
#for each name, make another hash table that links the name to its respective node number, name, latitude, and longitude.
        dict[row[1]] = {'node number' : row[0], 'name' : row[1], 'latitude' : row[2], 'longitude' : row[3]}


#print everything out!
for i in dict:
	print i

