#Let me walk you through this code.
#Import the PostgreSQL stuff
import psycopg2
	
try:
#Then we try to connect to the database with the credentials below. It is displayed when you try to ssh to the server.
	conn = psycopg2.connect("dbname='django' user='django' host='localhost' password='EBmpfDB8NN'")
except:
#The bottom line should never happen because we have the correct credentials.
	print "I am unable to connect to the database"

#We connect the cursor
cur = conn.cursor()

#The bottom line is the workhorse of this code. This is where the magic happens folks.
cur.execute("""	
	SELECT * from bostonunderwater_totem WHERE tier >= '0'
""")
#Technically, you can just do SELECT * from bostonunderwater_totem, but lets be redundant.


#rows is the output of the query.
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
print dict


#Here's an example of how you can use the magical "dict"
print "\n\n\n This is the edge of charles"
#This should return the name, latitude, longitude, and tier of 'edge of charles' node.
print dict['Edge of Charles']
#This should return the latitude of the 'edge of charles' node.
print dict['Edge of Charles']['latitude']
