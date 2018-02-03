# -*- coding: utf-8 -*-

import MySQLdb
import urllib
import urllib2
import re
import string
from bs4 import BeautifulSoup
from datetime import datetime

import time
import requests
import pprint
import json
import sys
import DBconnection



conn= DBconnection.connection()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))


def insert_gara_tutti(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        cursore = conn.cursor()
                        sql = """INSERT INTO gare.GARE_TUTTE (IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES (%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)"""
                        
                        
                        cursore.execute(sql, (identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download))                                                                   
                        
                        conn.commit()

def insert_gara_new(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        cursore = conn.cursor()
                        sql = """INSERT INTO gare.GARE_NEW (IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES (%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)"""
                        
                        
                        cursore.execute(sql, (identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download))                                                                   
                        
                        conn.commit() 



def gara_gia_inserita(data_scadenza, provincia, importo):
    conn= DBconnection.connection()
    curr = conn.cursor()
    importo_trunc = importo.split(',')[0]
    sql_esite = "SELECT * FROM gare.GARE_TUTTE where DATA_SCADENZA = '"+str(data_scadenza)+"' and PROVINCIA= '"+provincia+"' and IMPORTO like '"+importo_trunc+"%'"
    curr.execute(sql_esite)
    gare_new = curr.fetchall()
    ret = False
    if len(gare_new)>0:
        ret =  True
    conn.close()
    return ret   

def data_per_db(data):
    data=data.replace(u'\xa0', '')
    if data:               
        d = datetime.strptime(data, '%d/%m/%Y')
        day_string = d.strftime('%Y-%m-%d')
        
    else:
        day_string = "1900-01-01"
    return day_string


from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


#ecco
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}


formFields = (
)
def covert_in_timestamp(s):
    return time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())



curr = conn.cursor()

# CANCELLA DB NEW I VECCHI
sql_delete_gare_new = 'delete FROM gare.GARE_NEW where DATA_SCADENZA > NOW();'
curr.execute(sql_delete_gare_new)
conn.commit()


# ESISTENI
sql_esistenti ='SELECT * FROM gare.GARE_TUTTE;'
curr.execute(sql_esistenti)
IDENTIFICATIVI_records = curr.fetchall()
IDENTIFICATIVI_presenti = [cig[1]  for cig in IDENTIFICATIVI_records]

# ANAC
sql_ANAC ='SELECT * FROM gare.GARE_ANAC;'
curr.execute(sql_ANAC)
gare_ANAC = curr.fetchall()

num_gare = 0
for gara in gare_ANAC:
    IDENTIFICATIVO_gara = gara[1]
    if IDENTIFICATIVO_gara not in IDENTIFICATIVI_presenti:
        identificativo_gara = gara[1]
        provenienza = gara[2]
        cig = gara[3]
        oggetto = gara[4]
        tipologia = gara[5]
        procedura = gara[6]
        ente = gara[7]
        citta = gara[8]
        provincia = gara[9]
        regione = gara[10]
        importo = gara[11]
        data_inserimento = gara[12]
        data_pubblicazione = gara[13]
        data_scadenza = gara[14]
        cpv = gara[15]
        categoria_prevalente = gara[16]
        categorie_scorporabili = gara[17]
        info_aggiuntive = gara[18]
        download = gara[19]
        insert_gara_new(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento,data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        insert_gara_tutti(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        num_gare = num_gare + 1
            
            
print "INFO FINITO, INSERITE ANAC: "+ str(num_gare)


curr = conn.cursor()
# ESISTENI ANAC
sql_esistenti ='SELECT * FROM gare.GARE_TUTTE;'
curr.execute(sql_esistenti)
IDENTIFICATIVI_records = curr.fetchall()
IDENTIFICATIVI_presenti = [cig[1]  for cig in IDENTIFICATIVI_records]

# SCP 
sql_SCP ='SELECT * FROM gare.GARE_SCP;'
curr.execute(sql_SCP)
gare_SCP = curr.fetchall()

num_gare = 0
for gara in gare_SCP:
    IDENTIFICATIVO_gara = gara[1]
    if IDENTIFICATIVO_gara not in IDENTIFICATIVI_presenti:
        identificativo_gara = gara[1]
        provenienza = gara[2]
        cig = gara[3]
        oggetto = gara[4]
        tipologia = gara[5]
        procedura = gara[6]
        ente = gara[7]
        citta = gara[8]
        provincia = gara[9]
        regione = gara[10]
        importo = gara[11]
        data_inserimento = gara[12]
        data_pubblicazione = gara[13]
        data_scadenza = gara[14]
        cpv = gara[15]
        categoria_prevalente = gara[16]
        categorie_scorporabili = gara[17]
        info_aggiuntive = gara[18]
        download = gara[19]
        insert_gara_new(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento,data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        insert_gara_tutti(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        num_gare = num_gare + 1
            
            
print "INFO FINITO, INSERITE SCP: "+ str(num_gare)


# ETRU
# ESISTENI ANAC SCP GURI
sql_esistenti ='SELECT * FROM gare.GARE_TUTTE;'
curr.execute(sql_esistenti)
IDENTIFICATIVI_records = curr.fetchall()
IDENTIFICATIVI_presenti = [cig[1]  for cig in IDENTIFICATIVI_records]

sql_etru  = "SELECT * FROM gare.GARE_ETRU;"
curr.execute(sql_etru)
gare_ETRU = curr.fetchall()

num_gare = 0
for gara in gare_ETRU:
    IDENTIFICATIVO_gara = gara[1]
    if IDENTIFICATIVO_gara not in IDENTIFICATIVI_presenti:
        identificativo_gara = gara[1]
        provenienza = gara[2]
        cig = gara[3]
        oggetto = gara[4]
        tipologia = gara[5]
        procedura = gara[6]
        ente = gara[7]
        citta = gara[8]
        provincia = gara[9]
        regione = gara[10]
        importo = gara[11]
        data_inserimento = gara[12]
        data_pubblicazione = gara[13]
        data_scadenza = gara[14]
        cpv = gara[15]
        categoria_prevalente = gara[16]
        categorie_scorporabili = gara[17]
        info_aggiuntive = gara[18]
        download = gara[19]
        insert_gara_new(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento,data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        insert_gara_tutti(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        num_gare = num_gare + 1
print "INFO FINITO, INSERITE ETRU: "+ str(num_gare)



# GURI
# ESISTENI ANAC SCP
sql_esistenti ='SELECT * FROM gare.GARE_TUTTE;'
curr.execute(sql_esistenti)
IDENTIFICATIVI_records = curr.fetchall()
IDENTIFICATIVI_presenti = [cig[1]  for cig in IDENTIFICATIVI_records]


sql_guri  = "SELECT * FROM gare.GARE_GURI;"
curr.execute(sql_guri)
gare_GURI = curr.fetchall()

num_gare = 0
for gara in gare_GURI:
    IDENTIFICATIVO_gara = gara[1]
    if IDENTIFICATIVO_gara not in IDENTIFICATIVI_presenti:
        identificativo_gara = gara[1]
        provenienza = gara[2]
        cig = gara[3]
        oggetto = gara[4]
        tipologia = gara[5]
        procedura = gara[6]
        ente = gara[7]
        citta = gara[8]
        provincia = gara[9]
        regione = gara[10]
        importo = gara[11]
        data_inserimento = gara[12]
        data_pubblicazione = gara[13]
        data_scadenza = gara[14]
        cpv = gara[15]
        categoria_prevalente = gara[16]
        categorie_scorporabili = gara[17]
        info_aggiuntive = gara[18]
        download = gara[19]
        insert_gara_new(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento,data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        insert_gara_tutti(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        num_gare = num_gare + 1       
print "INFO FINITO, INSERITE GURI: "+ str(num_gare)



# INFO
# ESISTENI ANAC SCP GURI ETRU
sql_esistenti ='SELECT * FROM gare.GARE_TUTTE;'
curr.execute(sql_esistenti)
IDENTIFICATIVI_records = curr.fetchall()
IDENTIFICATIVI_presenti = [cig[1]  for cig in IDENTIFICATIVI_records]

sql_info  = "SELECT * FROM gare.GARE_INFO;"
curr.execute(sql_info)
gare_INFO = curr.fetchall()

num_gare = 0
for gara in gare_INFO:
    IDENTIFICATIVO_gara = gara[1]
    if IDENTIFICATIVO_gara not in IDENTIFICATIVI_presenti:
        identificativo_gara = gara[1]
        provenienza = gara[2]
        cig = gara[3]
        oggetto = gara[4]
        tipologia = gara[5]
        procedura = gara[6]
        ente = gara[7]
        citta = gara[8]
        provincia = gara[9]
        regione = gara[10]
        importo = gara[11]
        data_inserimento = gara[12]
        data_pubblicazione = gara[13]
        data_scadenza = gara[14]
        cpv = gara[15]
        categoria_prevalente = gara[16]
        categorie_scorporabili = gara[17]
        info_aggiuntive = gara[18]
        download = gara[19]
        insert_gara_new(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento,data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        insert_gara_tutti(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
        num_gare = num_gare + 1

print "INFO FINITO, INSERITE INFO: "+ str(num_gare)


