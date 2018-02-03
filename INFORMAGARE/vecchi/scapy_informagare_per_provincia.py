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

              


def insert_gara_informagare(cig,oggetto,tipologia,procedura,ente,citta,provincia,regione,importo,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP):
                        cursore = conn.cursor()
                        sql = 'INSERT INTO gare.GARE_INFORMA (cig,oggetto,tipologia,procedura,ente,citta,provincia,regione,importo,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP)   VALUES ("%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s")'% (cig,                                                
                                                                                              oggetto,
                                                                                              tipologia,
                                                                                              procedura,                                                                                                                                           
                                                                                              ente,
                                                                                              citta,
                                                                                              provincia,
                                                                                              regione,
                                                                                              importo,
                                                                                              data_pubblicazione,
                                                                                              data_scadenza,
                                                                                              cat_prev,
                                                                                              cat_scor1,
                                                                                              cat_scor2,
                                                                                              cat_scor3,
                                                                                              cat_scor4,
                                                                                              cat_scor5,
                                                                                              cpv,
                                                                                              bando_url,
                                                                                              bando_pdf,
                                                                                              ribasso,
                                                                                              criterio_agg,
                                                                                              data_agg,
                                                                                              importo_agg,
                                                                                              nr_offerte,
                                                                                              aggiudicatario,  
                                                                                              scaduto,
                                                                                              data_inserimento,
                                                                                              linkAVCP                                                                                                                                                                                                                                                                                                                                                                                                                            
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
    print sql_regione
    cursore.execute(sql_regione)
    record_regione = cursore.fetchone()
    regione = record_regione[1]
    #print regione
    
    serviceurl = 'http://www.informagare.it/risultato.php?regione=campania'
    s = requests.Session()
    s.post(serviceurl)

    serviceurl_prov =  "http://www.informagare.it/risultato.php?provincia="+rec[3]
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


            cig = ''
            oggetto = ''
            tipologia = ''
            procedura = ''
            ente = ''
            citta = ''

            importo_fin = ''
            data_pubblicazione = ''
            data_scadenza = ''
            cat_prev = ''
            cat_scor1 = ''
            cat_scor2 = ''
            cat_scor3 = ''
            cat_scor4 = ''
            cat_scor5 = ''
            cpv = ''
            bando_url = ''
            bando_pdf = ''
            ribasso = ''
            criterio_agg = ''
            data_agg = ''
            importo_agg = ''
            nr_offerte = ''
            aggiudicatario = ''
            scaduto = ''
            data_inserimento = ''
            linkAVCP  = ''
            
            iden = celle[2].get_text().strip()

            cig = iden+'_INFOGARE'
            
            scadenza = celle[3].get_text()

            data_scadenza = data_per_db(scadenza.strip())
            
            ente = celle[4].get_text().strip()
            ente = ente.replace('"','')
                
            regione_dentro = celle[5].get_text().replace(',','').strip()
            if 'italia' in regione_dentro:
               regione = 'ITALIA'
               provincia = 'TT'
               

            oggetto_tutti = celle[6].get_text().strip()
            info_oggetti = oggetto_tutti.split('.')
            """
            oggetto = ''
            for info in info_oggetti:
                if len(info)>0:
                    if info[0] != ' ':
                        if info[0] != '(':
                            oggetto = oggetto + info
            """
            if len(info_oggetti[0]) < 30:
                oggetto = oggetto_tutti[:100]+'...'
                oggetto = oggetto.replace('"','')
            else:
                oggetto = info_oggetti[0].replace('"','')

            if 'COMUNE DI ' in oggetto_tutti.upper():
                oggetto_tutti = oggetto_tutti.upper()

                citta =  oggetto_tutti.split('COMUNE DI ')[1].split('.')[0].split(',')[0].split('(')[0].split(';')[0].split(' ')[0]
                citta = citta.replace('o','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
                ente = 'COMUNE DI ' + citta


            # categoria prevalente + info
            cpv = ''
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
                


            cat_scor1 = ''
            cat_scor2= ''
            cat_scor3= ''
            cat_scor4= ''
            cat_scor5= ''
            cat_scorps = celle[8].get_text().strip()

            cat_scorps_list =  cat_scorps.split(',')
            if len(cat_scorps_list) > 1:
                cat_scor1 = cat_scorps_list[0].strip()
            if len(cat_scorps_list) > 2:
                cat_scor1 = cat_scorps_list[1].strip()
            if len(cat_scorps_list) > 3:
                cat_scor1 = cat_scorps_list[2].strip()
            if len(cat_scorps_list) > 4:
                cat_scor1 = cat_scorps_list[3].strip()
            # importo + procedura_dett
            importo = celle[9]
            celle_importo = importo.find_all("strong")
            importo_fin = celle_importo[0].get_text().strip()
            if len(celle_importo)>1:
                 procedura_dett = celle_importo[1]
                 #print str(procedura_dett).replace('<br/>',' ').replace('<strong><span align="left" class="grande_10">','').replace('</span></strong>','')
            #print importo_fin


            
            procedura = str(celle[10]).replace('<br/>',' ').replace('<td>','').replace('</td>','').strip()
            #print str(procedura).replace('<br/>',' ').replace('<td>','').replace('</td>','').strip()
            dettagli = celle[11].get_text()
            #print dettagli

            """
            print "*******RIGA*********+"
            print cig
            print oggetto.upper()
            print tipologia.upper()
            print procedura.upper()
            print ente.upper()
            print citta.upper()
            print provincia.upper()
            print regione.upper()
            print importo_fin
            print data_pubblicazione
            print data_scadenza
            print cat_prev
            print cat_scor1
            print cat_scor2
            print cat_scor3
            print cat_scor4
            print cat_scor5
            print cpv
            print bando_url
            
            print "__________________________"
            """




            d = dt.datetime.now()
            data_inserimento = d.strftime('%Y-%m-%d')

            
            sql_exist = "SELECT * FROM gare.GARE_INFORMA where CIG = '"+cig+"'"
            cursore = conn.cursor()
            lista_url = []
            cursore.execute(sql_exist)
            cig_exist = cursore.fetchall()

            
            if cig not in lista_gia_inclusi and len(cig_exist) == 0:
                insert_gara_informagare(cig,oggetto.upper(),tipologia.upper(),procedura.upper(),ente.upper(),citta.upper(),provincia.upper(),regione.upper(),importo_fin,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP)
                print cig , "INSERITO"
            else:
                print cig , "NON INSERITO"


