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
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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


#print duckduckgo.get_zci('ASL Salerno')

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
  "apiKey": "AIzaSyAecCiVjizFOWgZM4KuSpdzDcyyEw1MBl0",
  "authDomain": "bandigare-8096d.firebaseapp.com",
  "databaseURL": "https://bandigare-8096d.firebaseio.com",
  "storageBucket": "bandigare-8096d.appspot.com",
  "messagingSenderId": "1009811970424"
}


from firebase import firebase
firebase = firebase.FirebaseApplication('https://bandigare-8096d.firebaseio.com', None)

firebase.delete('/gare', None)

testo_mail = ""

conn= DBconnection.connection()
cursore = conn.cursor()


# AGGIUNGE LE GARE NUOVE
gare_da_inserire = {}

# CARICA LE GARE NON SCADUTE E CHE HANNO ENTE
cursore.execute("SELECT * FROM gare.GARE_TUTTE WHERE DATA_SCADENZA >NOW() and ENTE <>''") 
gare = cursore.fetchall()
num_inserite = 0
gare_da_mischiare= []
for uno in gare:
    gare_da_mischiare.append(uno)

gare_mischiate = random.sample(gare_da_mischiare, len(gare_da_mischiare))

for gara in gare_mischiate:
    if 1:
        try:
            iden =  'ID'+str(gara[0])
            gara_json = prendi_json(gara)
            gare_da_inserire[iden] = gara_json
            num_inserite = num_inserite + 1 
        except:
            iden =  'ID'+str(gara[0])
            gara_pulita = pulisci_gara(gara)
            gara_json = prendi_json(gara_pulita)
            gare_da_inserire[iden] = gara_json
            num_inserite = num_inserite + 1 

#SELECT count(*) FROM gare.GARE_TUTTE where DATA_SCADENZA > NOW() and ENTE <> '' 
result = firebase.put('','/gare', gare_da_inserire)
print "Numero gare inserite in firebase: " + str(num_inserite)



# ELIMINA GARE SCADUTE FIREBASE	
d = dt.datetime.now()
oggi = d.strftime('%Y-%m-%d')
timestamp_oggi = convert_in_timestamp(oggi)
tutte_le_gare = firebase.get('/gare', None)
num_eliminate = 0
for res in tutte_le_gare:
    if res:
        chiave = res
        valore = tutte_le_gare[chiave]
        if  valore['DATA_SCADENZA'] < timestamp_oggi:
            firebase.delete('/gare', chiave)
            num_eliminate = num_eliminate + 1
print "Numero gare eliminate firebase: " + str(num_eliminate)




# ELIMINA GARE ANAC

sql_ANAC = "SELECT count(*) FROM gare.GARE_ANAC;"
cursore.execute(sql_ANAC)
num_gare_ANAC = cursore.fetchone()
print "Numero gare ANAC: " + str(num_gare_ANAC[0])
testo_ANAC = "Numero gare ANAC: " + str(num_gare_ANAC[0]) + '\n'

sql_delete_now = 'DELETE FROM gare.GARE_ANAC;'
cursore.execute(sql_delete_now)
conn.commit()


# ELIMINA GARE SCP
sql_SCP = "SELECT count(*) FROM gare.GARE_SCP;"
cursore.execute(sql_SCP)
num_gare_SCP = cursore.fetchone()
print "Numero gare SCP: " + str(num_gare_SCP[0])
testo_SCP = "Numero gare SCP: " + str(num_gare_SCP[0]) + '\n'

sql_delete_now = 'DELETE FROM gare.GARE_SCP;'
cursore.execute(sql_delete_now)
conn.commit()

# ELIMINA GARE GURI
sql_GURI = "SELECT count(*) FROM gare.GARE_GURI;"
cursore.execute(sql_GURI)
num_gare_GURI = cursore.fetchone()
print "Numero gare GURI: " + str(num_gare_GURI[0])
testo_GURI = "Numero gare GURI: " + str(num_gare_GURI[0]) + '\n'

sql_delete_now = 'DELETE FROM gare.GARE_GURI;'
cursore.execute(sql_delete_now)
conn.commit()

# ELIMINA GARE ETRU
sql_ETRU = "SELECT count(*) FROM gare.GARE_ETRU;"
cursore.execute(sql_ETRU)
num_gare_ETRU = cursore.fetchone()
print "Numero gare ETRU: " + str(num_gare_ETRU[0])
testo_ETRU = "Numero gare ETRU: " + str(num_gare_ETRU[0]) + '\n'

sql_delete_now = 'DELETE FROM gare.GARE_ETRU;'
cursore.execute(sql_delete_now)
conn.commit()

# ELIMINA GARE INFO
sql_INFO = "SELECT count(*) FROM gare.GARE_INFO;"
cursore.execute(sql_INFO)
num_gare_INFO = cursore.fetchone()
print "Numero gare INFO: " + str(num_gare_INFO[0])
testo_INFO = "Numero gare INFO: " + str(num_gare_INFO[0]) + '\n'

sql_delete_now = 'DELETE FROM gare.GARE_INFO;'
cursore.execute(sql_delete_now)
conn.commit()

testo_mail = testo_ANAC + testo_SCP+  testo_GURI+ testo_ETRU+ testo_INFO
invia_mail("Resoconto Gare", testo_mail)

print "CANCELLATI I DATABASE DELLE GARE"
conn.close()

