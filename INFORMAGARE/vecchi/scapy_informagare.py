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

#serviceurl = "http://www.informagare.it/riepiloghi_ultimi_sette.php?regione=campania"
#serviceurl = "http://www.informagare.it/risultato.php?regione=campania"

# TUTTI I LINK PER REGIONE
sql_regioni = "SELECT * FROM gare.regioni;"
cursore = conn.cursor()
lista_url = []
cursore.execute(sql_regioni)
records_regioni = cursore.fetchall()
for rec in records_regioni:
    lista_url.append("http://www.informagare.it/risultato.php?regione="+rec[1].replace(' ','%20').replace("'",'%20'))


# IDENTIFICATIVI INCLUSI
lista_gia_inclusi = []
sql_valutati = "SELECT * FROM gare.GARE_INFORMA;"
cursore = conn.cursor()
lista_valutati = []
cursore.execute(sql_valutati)
records_valutati = cursore.fetchall()
for rec in records_valutati:
    lista_gia_inclusi.append(rec[0])


#print lista_gia_inclusi

#lista_url = ['http://www.informagare.it/risultato.php?regione=Campania']
for serviceurl in lista_url:
    print serviceurl

    r = requests.post(serviceurl)
    testoHTML = r.text

    soup = BeautifulSoup(testoHTML)
    tabelle = soup.find_all("table", attrs={"class": "modulo", "width": "850"})
    tabella =  tabelle[0]

    righe = tabella.find_all("tr")[1:]
    for riga in righe:



        celle = riga.find_all("td")
        
        if (len(celle)>7):


            cig = ''
            oggetto = ''
            tipologia = ''
            procedura = ''
            ente = ''
            citta = ''
            provincia = ''
            regione = ''
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
                
            regione = celle[5].get_text().replace(',','').strip()

            oggetto_tutti = celle[6].get_text().strip()
            info_oggetti = oggetto_tutti.split('.')

            oggetto = ''
            for info in info_oggetti:
                if len(info)>0:
                    if info[0] != ' ':
                        if info[0] != '(':
                            oggetto = oggetto + info
            oggetto = oggetto.replace('"','')


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
            if cig not in lista_gia_inclusi:
                insert_gara_informagare(cig,oggetto.upper(),tipologia.upper(),procedura.upper(),ente.upper(),citta.upper(),provincia.upper(),regione.upper(),importo_fin,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP)
                print cig , "INSERITO"
            else:
                print cig , "NON INSERITO"

