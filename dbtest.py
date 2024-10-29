import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='',
    db='djangocrm',
    ssl={'ca': '', 'cert': '', 'key': ''}
)

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : %s " % data)
db.close()
