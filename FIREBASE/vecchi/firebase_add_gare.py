from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import MySQLdb
import urllib
import urllib2
import re
import string
from bs4 import BeautifulSoup

import datetime
import calendar
import time
import os
import json as m_json

import requests
import pyrebase
import time
import datetime as dt

import DBconnection

def convert_in_timestamp(data_stringa):
    if len(data_stringa)>9 and data_stringa != '1900-01-01':
        return time.mktime(datetime.datetime.strptime(data_stringa, "%Y-%m-%d").timetuple())
    else:
        return 0 


#print duckduckgo.get_zci('ASL Salerno')

def prendi_json(gara):
    data = {}
    data["ID"] = gara[0]
    data["IDENTIFICATIVO_GARA"] = gara[1].decode('cp1252')
    data["PROVENIENZA"] = gara[2].decode('cp1252')
    data["CIG"] = gara[3].decode('cp1252')
    data["OGGETTO"] = gara[4].decode('cp1252')
    data["TIPOLOGIA"] = gara[5].decode('cp1252')
    data["PROCEDURA"] = gara[6].decode('cp1252')
    data["ENTE"] = gara[7].decode('cp1252')
    data["CITTA"] = gara[8]
    data["PROVINCIA"] = gara[9]
    data["REGIONE"] = gara[10]
    data["IMPORTO"] = gara[11]
    data["DATA_INSERIMENTO"] = convert_in_timestamp(str(gara[12]))
    data["DATA_PUBBLICAZIONE"] = convert_in_timestamp(str(gara[13]))
    data["DATA_SCADENZA"] = convert_in_timestamp(str(gara[14]))
    data["CPV"] = gara[15]
    data["CATEGORIA_PREVALENTE"] = gara[16]
    data["CATEGORIE_SCORPORABILI"] = gara[17]
    data["INFO_AGGIUNTIVE"] = gara[18]
    data["DOWNLOAD"] = gara[19]
    return data

config = {
  "apiKey": "AIzaSyAecCiVjizFOWgZM4KuSpdzDcyyEw1MBl0",
  "authDomain": "bandigare-8096d.firebaseapp.com",
  "databaseURL": "https://bandigare-8096d.firebaseio.com",
  "storageBucket": "bandigare-8096d.appspot.com",
  "messagingSenderId": "1009811970424"
}


firebase = pyrebase.initialize_app(config)
conn= DBconnection.connection()
db = firebase.database()
cursore = conn.cursor()


# ELIMINA LE GARE SCADUTE DA GARE NOW
sql_delete_now = 'DELETE FROM gare.GARE_NEW where DATA_SCADENZA < NOW()'
cursore.execute(sql_delete_now)
conn.commit()


# AGGIUNGE LE GARE NUOVE

cursore.execute("SELECT * FROM gare.GARE_NEW;")
gare = cursore.fetchall()
num_inserite = 0
for gara in gare:
    try:
        dati = prendi_json(gara)
        db.child("gare").push(dati)
        num_inserite = num_inserite + 1
    except:
        print "ERRORE IN GARA", gara[1]
print "Numero gare inserite in firebase: " + str(num_inserite)


# ELIMINA GARE SCADUTE FIREBASE	
d = dt.datetime.now()
oggi = d.strftime('%Y-%m-%d')
timestamp_oggi = convert_in_timestamp(oggi)
all_gare = db.child("gare").get()
num_eliminate = 0
for gara in all_gare.each():
    chiave =  gara.key()
    valore =  gara.val()
    if  valore['DATA_SCADENZA'] < timestamp_oggi:
        db.child("gare").child(chiave).remove()
        num_eliminate = num_eliminate + 1
print "Numero gare eliminate firebase: " + str(num_eliminate)




# ELIMINA GARE ANAC
sql_delete_now = 'DELETE FROM gare.GARE_ANAC;'
cursore.execute(sql_delete_now)
conn.commit()


# ELIMINA GARE SCP
sql_delete_now = 'DELETE FROM gare.GARE_SCP;'
cursore.execute(sql_delete_now)
conn.commit()

# ELIMINA GARE GURI
sql_delete_now = 'DELETE FROM gare.GARE_GURI;'
cursore.execute(sql_delete_now)
conn.commit()

# ELIMINA GARE ETRU
sql_delete_now = 'DELETE FROM gare.GARE_ETRU;'
cursore.execute(sql_delete_now)
conn.commit()

# ELIMINA GARE INFO
sql_delete_now = 'DELETE FROM gare.GARE_INFO;'
cursore.execute(sql_delete_now)
conn.commit()

print "CANCELLATI I DATABASE DELLE GARE"
