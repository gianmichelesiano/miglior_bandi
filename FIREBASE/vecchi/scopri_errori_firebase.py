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


def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

from firebase import firebase
firebase = firebase.FirebaseApplication('https://bandigare-8096d.firebaseio.com', None)


conn= DBconnection.connection()
cursore = conn.cursor()


def pulisci_gara(gara):
    gara_pulita = []
    
    for una in gara:
        if type(una) == str:
            gara_pulita.append(removeNonAscii(str(una)))
        else:
            gara_pulita.append(una)
    return gara_pulita

identificativo_gara = '193330_INFO'
if 1:

            sql_exist = "SELECT * FROM gare.GARE_TUTTE where IDENTIFICATIVO_GARA =  '"+identificativo_gara+"'"
            cursore = conn.cursor()
            lista_url = []
            cursore.execute(sql_exist)
            cig_exist = cursore.fetchall()

print len(cig_exist)

lista_gia_inclusi = []

if identificativo_gara not in lista_gia_inclusi and len(cig_exist) == 0:
    print "mammt"
"""
# AGGIUNGE LE GARE NUOVE
cursore.execute("SELECT * FROM gare.GARE_NEW where IDENTIFICATIVO_GARA = '193330_INFO' limit 1")
gare = cursore.fetchall()
num_inserite = 0

for gara in gare:
    print gara
    if 1:
        if 1:
            gara_json = prendi_json(gara)
            result = firebase.post('/gare', gara_json)
            num_inserite = num_inserite + 1
"""
   

