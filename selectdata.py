'''
This script connects to the database and runs a simple select from where query in 
postgresql!
'''
import psycopg2
	
try:
	conn = psycopg2.connect("dbname='django' user='django' host='localhost' password='EBmpfDB8NN'")
except:
	print "I am unable to connect to the database"

cur = conn.cursor()
cur.execute("""	
	SELECT * from bostonunderwater_totem WHERE tier >= '0'
""")


rows = cur.fetchall()
dict = {}

print "\n Show me the databases: \n"
for row in rows:
	dict[row[1]] = {'node number' : row[0], 'name' : row[1], 'latitude' : row[2], 'longitude' : row[3]}

print dict


print "\n\n\n This is the edge of charles"
print dict['Edge of Charles']
print dict['Edge of Charles']['latitude']
