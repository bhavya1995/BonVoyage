import xlrd
import pymysql
import settings

conn = pymysql.connect(host=settings.DATABASES['default']['HOST'], port=int(settings.DATABASES['default']['PORT']), user=settings.DATABASES['default']['USER'], passwd=settings.DATABASES['default']['PASSWORD'], db=settings.DATABASES['default']['NAME'],autocommit='true')
cur = conn.cursor()

book = xlrd.open_workbook('/home/bhavya/web/bon-voyage/bonvoyage/bonvoyage/country_code_web.xls')

# print number of sheets
print(book.nsheets)

# print(sheet names
print(book.sheet_names())

# get the first worksheet
first_sheet = book.sheet_by_index(0)

# read a row
print(first_sheet.row_values(0))

# read a cell
cell = first_sheet.cell(3,0)
counter = 3
sql = ""
while (counter <= 238):
    try:
        sql = "INSERT INTO travelRequirement_isocode (country, code) VALUES ('" + first_sheet.cell(counter,0).value + "','" + first_sheet.cell(counter,1).value + "');"
        cur.execute(sql)
        conn.commit()
    except:
        pass
    counter += 1
    print(sql)
    
print(cell)
print(cell.value)

# read a row slice
print(first_sheet.row_slice(rowx=0,
                            start_colx=0,
                            end_colx=2))
