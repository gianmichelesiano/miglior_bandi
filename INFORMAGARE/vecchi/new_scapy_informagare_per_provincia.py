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
import datetime as dt



conn= DBconnection.connection()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

              
def prendi_import(imp):
    #imp = '€ 40.810.000'

    impor = imp.replace('.','').replace(' ','')
    return impor


def get_link(ente, citta):
        link = ''
        try:
                cursore = conn.cursor()
                sql_link = 'SELECT LINK FROM gare.LINK_ENTI where ente  = "'+ente+'"'
                cursore.execute(sql_link)
                data=cursore.fetchall()
                if len(data)>0:
                        link = data[0][0]
                else:
                        keywords = ente + " " + citta
                        risultati_duck = search_duckduckgo(keywords, max_results=1)
                        time.sleep(5)
                        for ris in risultati_duck:
                                link = ris
        except:
                pass
        return link


def insert_gara_info(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        cursore = conn.cursor()
                        sql = """INSERT INTO gare.GARE_INFO (IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES ("%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s", "%s","%s",'%s','%s')"""% (identificativo_gara,
                                                                                              provenienza,
                                                                                              cig,                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                              oggetto,
                                                                                              tipologia,
                                                                                              procedura,                                                                                                                                           
                                                                                              ente,
                                                                                              citta,
                                                                                              provincia,
                                                                                              regione,
                                                                                              importo,
                                                                                              data_inserimento,                                                                                                                                                                                                                                                                                                                                                                                                                               
                                                                                              data_pubblicazione,
                                                                                              data_scadenza,
                                                                                              cpv,                                                                                                                                                                      
                                                                                              categoria_prevalente,
                                                                                              categorie_scorporabili,
                                                                                              info_aggiuntive,
                                                                                              download                                                                                                                                                                                                                                                                                                                                                                                                                         
                                                                                              )
                        #print sql
                                                                                           
                        cursore.execute(sql)
                        conn.commit()





def data_per_db(data):
    data=data.replace(u'\xa0', '')
    if data:               
        d = datetime.strptime(data, '%d/%m/%Y')
        day_string = d.strftime('%Y-%m-%d')
        
    else:
        day_string = "1900-01-01"
    return day_string


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


# IDENTIFICATIVI INCLUSI
lista_gia_inclusi = []
sql_valutati = "SELECT * FROM gare.GARE_INFORMA;"
cursore = conn.cursor()
lista_valutati = []
cursore.execute(sql_valutati)
records_valutati = cursore.fetchall()
for rec in records_valutati:
    lista_gia_inclusi.append(rec[0])



# TUTTI I LINK PER REGIONE
sql_provincie = "SELECT * FROM gare.province_sigle;"
cursore = conn.cursor()
lista_url = []
cursore.execute(sql_provincie)
records_provincie = cursore.fetchall()


#records_provincie = [(1,'Ancona',1,'AN')]
for rec in records_provincie:
    provincia = rec[3]
    print provincia
    
    sql_regione = "SELECT * FROM gare.regioni_da_prov where nome_province like '%"+provincia+"%'"
    #print sql_regione
    cursore.execute(sql_regione)
    record_regione = cursore.fetchone()
    regione = record_regione[1]
    #print regione
    
    serviceurl = 'http://www.informagare.it/risultato.php?regione=campania'
    s = requests.Session()
    s.post(serviceurl)

    serviceurl_prov =  "http://www.informagare.it/risultato.php?provincia="+rec[3]
    print serviceurl_prov
    r2 = s.get(serviceurl_prov)

    testoHTML = r2.text


    soup = BeautifulSoup(testoHTML)
    tabelle = soup.find_all("table", attrs={"class": "modulo", "width": "850"})
    tabella =  tabelle[0]

    righe = tabella.find_all("tr")[1:]
    for riga in righe:

        provincia = rec[3]
        regione = record_regione[1]

        celle = riga.find_all("td")
        
        if (len(celle)>7):
            provenienza = 'ETRU'
            # CIG, PROVENIENZA
            cig = ''
            cig = celle[2].get_text().strip()
            identificativo_gara = cig+'_INFO'

            # OGGETTO
            oggetto = ''
            oggetto_tutti = celle[6].get_text().strip()
            info_oggetti = oggetto_tutti.split('.')
            if len(info_oggetti[0]) < 30:
                oggetto = oggetto_tutti[:100]+'...'
                oggetto = oggetto.replace('"','')
            else:
                oggetto = info_oggetti[0].replace('"','')
            

            # TIPOLOGIA
            cpv = ''
            cat_prev = ''
            tipologia = 'LAVORI'
            cat_prev = celle[7].strong.get_text().replace('/n','').replace(' ','').replace('_','')
            if cat_prev == 'iscrizionealbo':
                tipologia = 'SERVIZI'
                cpv = '45'
                cat_prev = "Lavori di costruzione".upper()
            if cat_prev == 'servizitecnici':
                tipologia = 'SERVIZI'
                cpv = '71'
                cat_prev = "Servizi architettonici e ingegneria".upper()
            if cat_prev == 'servizirifiuti':
                tipologia = 'SERVIZI'
                cpv = '90'
                cat_prev = "Servizi ambientali".upper()
            if cat_prev == 'servizidipulizia':
                tipologia = 'SERVIZI'
                cpv = '79'
                cat_prev = "Servizi di pulizia".upper()
            if cat_prev == 'servizicimiteriali':
                tipologia = 'SERVIZI'
                cpv = '63'
                cat_prev = "Servizi cimiteriali".upper()
            if cat_prev == 'manutenz.impianti':
                tipologia = 'SERVIZI'
                cpv = '63'
                cat_prev = "Servizi di manutenzione".upper()
            if cat_prev == 'foniaevideo':
                tipologia = 'SERVIZI'
                cpv = '64'
                cat_prev = "Servizi di telecomunicazione".upper()

            # PROCEDURA
            procedura = ''
            procedura = str(celle[10]).replace('<br/>',' ').replace('<td>','').replace('</td>','').strip()

            # ENTE
            ente = ''
            ente = celle[4].get_text().strip()
            ente = ente.replace('"','')

            # CITTA, PROVINCIA, REGIONE
            citta = ''

            if 'COMUNE DI ' in oggetto_tutti.upper():
                oggetto_tutti = oggetto_tutti.upper()
                citta =  oggetto_tutti.split('COMUNE DI ')[1].split('.')[0].split(',')[0].split('(')[0].split(';')[0].split(' ')[0]
                citta = citta.replace('o','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
                ente = 'COMUNE DI ' + citta

            # IMPORTO
            importo  = ''
            importo = celle[9]
            celle_importo = importo.find_all("strong")
            importo_fin = celle_importo[0].get_text().strip()
            importo = prendi_import(importo_fin)            
                
            # DATA INSERIMENTO
            d = dt.datetime.now()
            data_inserimento = d.strftime('%Y-%m-%d')

            # DATA INSERIMENTO
            data_pubblicazione = ''

            # DATA INSERIMENTO
            data_scadenza = ''
            scadenza = celle[3].get_text()
            data_scadenza = data_per_db(scadenza.strip())

            # CPV CALCOLATO SU IN TIPOLOGIA
            cpv = cpv
            

            # CATEGORIA PREVALENTE
            categoria_prevalente = cat_prev 
            
            # CATEGORIA SCORPORABILE
            categorie_scorporabili = celle[8].get_text().strip()

            
            # CATEGORIA INFO AGGIUNTIVE
            info_aggiuntive_dict =  {}
            info_aggiuntive_dict['link'] = get_link(ente, citta)
            info_aggiuntive = json.dumps(info_aggiuntive_dict)            
            
            # CATEGORIA DOWNLOAD
            download = ''

            #print identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download
            time.sleep(5)

           
            sql_exist = "SELECT * FROM gare.GARE_INFO where CIG = '"+cig+"'"
            cursore = conn.cursor()
            lista_url = []
            cursore.execute(sql_exist)
            cig_exist = cursore.fetchall()

            
            if cig not in lista_gia_inclusi and len(cig_exist) == 0:
                insert_gara_info(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
                print cig , "INSERITO"
            else:
                print cig , "NON INSERITO"


