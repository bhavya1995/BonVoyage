from urllib.request import urlopen
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='bhavya', db='bonvoyage',autocommit='true')
cur = conn.cursor()
content = urlopen("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat")
html = content.read()
arr = html.splitlines()
for a in arr:
	data = a.decode("utf-8")
	attributes = data.split(",")
	print(attributes[0])
	try:
		sql="INSERT INTO travelRequirement_airportdetails (name, city, country, code) VALUES (%s,%s,%s,%s);" % (attributes[1], attributes[2], attributes[3], attributes[4])
		cur.execute(sql)
		conn.commit()
	except:
		pass
	