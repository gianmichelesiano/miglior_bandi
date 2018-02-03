import DBconnection
conn= DBconnection.connection()
import time

sql = 'SELECT * FROM gare.province_sigle;'
cursore = conn.cursor()
cursore.execute(sql)
tutte  =  cursore.fetchall()

dizo = { }
for una in tutte:
    print una[1], una[-1]
    dizo[una[-1]] = una[1]
    
print dizo

