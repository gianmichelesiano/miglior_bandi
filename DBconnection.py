import MySQLdb
#myDB = MySQLdb.connect(host="192.168.1.108",port=3306,user="username",passwd="password",db="")
def connection():
    myDB = MySQLdb.connect(host="192.168.1.115",port=3306,user="username",passwd="password",db="")
    myDB.ping(True)
    return myDB



