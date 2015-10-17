from urllib.request import urlopen
import pymysql
import settings

conn = pymysql.connect(host=settings.DATABASES['default']['HOST'], port=int(settings.DATABASES['default']['PORT']), user=settings.DATABASES['default']['USER'], passwd=settings.DATABASES['default']['PASSWORD'], db=settings.DATABASES['default']['NAME'],autocommit='true')
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
	
