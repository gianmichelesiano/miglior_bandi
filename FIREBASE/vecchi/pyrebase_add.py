import pyrebase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import MySQLdb
import urllib
import urllib2
import re
import smtplib
import string
from bs4 import BeautifulSoup
import datetime as dt
import calendar
import time
import os
import json as m_json
import requests
import time
from datetime import datetime
import DBconnection
import random
from firebase import firebase

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))


def invia_mail(soggetto, testo):
    gmail_user = 'bandigare@gmail.com'  
    gmail_password = 'Wolfgang-75'

    toaddr = "gianmichele.siano@gmail.com"


    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = toaddr
    msg['Subject'] = soggetto
    body = testo
    msg.attach(MIMEText(body, 'plain'))


    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, toaddr, text)
        server.close()

        print 'Email sent!'
    except:  
        print 'Something went wrong...'

def pulisci_gara(gara):
    gara_pulita = []
    for una in gara:
        if type(una) == str:
            gara_pulita.append(removeNonAscii(str(una)))
        else:
            gara_pulita.append(una)
    return gara_pulita

def convert_in_timestamp(data_stringa):
    if len(data_stringa)>9 and data_stringa != '1900-01-01':
        try:
            return time.mktime(dt.datetime.strptime(data_stringa, "%Y-%m-%d").timetuple())
        except:
            return 0 
    else:
        return 0


def prendi_json(gara):
    data = {}
    data["ID"] = gara[0]
    data["IDENTIFICATIVO_GARA"] = gara[1].decode('cp1252').encode('utf-8')
    data["PROVENIENZA"] = gara[2].decode('cp1252').encode('utf-8')
    data["CIG"] = gara[3].decode('cp1252').encode('utf-8')
    data["OGGETTO"] = gara[4].decode('cp1252').encode('utf-8')
    data["TIPOLOGIA"] = gara[5].decode('cp1252').encode('utf-8')
    data["PROCEDURA"] = gara[6].decode('cp1252').encode('utf-8')
    data["ENTE"] = gara[7].decode('cp1252').encode('utf-8')
    data["CITTA"] = gara[8].decode('cp1252').encode('utf-8')
    data["PROVINCIA"] = gara[9].decode('cp1252').encode('utf-8')
    data["REGIONE"] = gara[10].decode('cp1252').encode('utf-8')
    data["IMPORTO"] = gara[11].decode('cp1252').encode('utf-8')
    data["DATA_INSERIMENTO"] = convert_in_timestamp(str(gara[12]))
    data["DATA_PUBBLICAZIONE"] = convert_in_timestamp(str(gara[13]))
    data["DATA_SCADENZA"] = convert_in_timestamp(str(gara[14]))
    data["CPV"] = gara[15].decode('cp1252').encode('utf-8')
    data["CATEGORIA_PREVALENTE"] = gara[16].decode('cp1252').encode('utf-8')
    data["CATEGORIE_SCORPORABILI"] = gara[17].decode('cp1252').encode('utf-8')
    data["INFO_AGGIUNTIVE"] = gara[18].decode('cp1252').encode('utf-8')
    data["DOWNLOAD"] = gara[19].decode('cp1252').encode('utf-8')
    return data

config = {
  "apiKey": "AIzaSyANnvFxDaqqdlp5Hb0CP2hKLvqiXXQOASE",
  "authDomain": "altro-78ee0.firebaseapp.com",
  "databaseURL": "https://altro-78ee0.firebaseio.com",
  "storageBucket": "944259960945"
}

# delete
"""
firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.child("gare").remove()
"""


testo_mail = ""
conn= DBconnection.connection()
cursore = conn.cursor()

firebase = pyrebase.initialize_app(config)
db = firebase.database()
gare_da_inserire = {}

cursore.execute("SELECT * FROM gare.GARE_NEW limit 5000;")
gare = cursore.fetchall()
num_inserite = 0
gare_da_mischiare= []

for uno in gare:
    gare_da_mischiare.append(uno)
random.shuffle(gare_da_mischiare)    
for gara in gare_da_mischiare:
    if 1:
        try:
            gara_json = prendi_json(gara)
            gare_da_inserire[gara_json["ID"]] = gara_json
            num_inserite = num_inserite + 1

        except:
            gara_pulita = pulisci_gara(gara)
            gare_da_inserire[gara_json["ID"]] = gara_json



db.child("gare").set(gare_da_inserire)





 
