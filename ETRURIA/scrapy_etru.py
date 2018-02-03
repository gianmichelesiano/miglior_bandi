# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import MySQLdb
import urllib
import urllib2
import re
import string
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt
import calendar
import time
import os
import json as m_json
import duckduckgo
import requests
import pprint
import json
import sys
from lxml import html

import smtplib
import re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import DBconnection



conn= DBconnection.connection()


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

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))



def search_duckduckgo(keywords, max_results=None):
	url = 'https://duckduckgo.com/html/'
	params = {
		'q': keywords,
		's': '0',
	}

	serviceurl = 'https://duckduckgo.com'
	s = requests.Session()
	s.post(serviceurl)

	yielded = 0
	while True:
		res = s.post(url, data=params)
		doc = html.fromstring(res.text)

		results = [a.get('href') for a in doc.cssselect('#links .links_main a')]
		for result in results:
			yield result
			time.sleep(0.1)
			yielded += 1
			if max_results and yielded >= max_results:
				return

		try:
			form = doc.cssselect('.results_links_more form')[-1]
		except IndexError:
			return
		params = dict(form.fields)



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


def converti_data (data_py):
        data_ita = data_py.strftime('%d-%m-%Y')
        sitrng = str(data_ita)
        return data_ita





def data_per_db(data):
    data=data.replace(u'\xa0', '')
    if data:               
        d = datetime.strptime(data, '%d/%m/%Y')
        day_string = d.strftime('%Y-%m-%d')
        
    else:
        day_string = "1900-01-01"
    return day_string
        
        
    

def prendi_import(imp):
    #imp = '€ 40.810.000'
    impor = imp.replace('.','').replace(' ','')
    val = impor.split(",")

    if len(val) > 1:
        decimale = val[1][:2]
    else:
        decimale = "00"
    tot = val[0] +','+ decimale
    return tot





def insert_gara_etru(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        cursore = conn.cursor()
                        sql = """INSERT INTO gare.GARE_ETRU (IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES ("%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s", "%s","%s",'%s','%s')"""% (identificativo_gara,
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







#ecco
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}


formFields = (
)



# CANCELLA DB NEW
curr = conn.cursor()
sql_delete_gare_etru = 'delete FROM gare.GARE_ETRU;'
curr.execute(sql_delete_gare_etru)
conn.commit()


# da cercare cig, tipologia gara, proceduna , citta

serviceurl = "http://app.appalti-app.it/service/service.php"



index = 0
flag = True
while flag:  
    payload = { 'tipo':'elenco_gare_attive', 'idutente' : '' , 'from':0 }
    payload['from'] = index
    print serviceurl
    print payload
    r = requests.post(serviceurl, data=payload)
    
    responce_json = json.loads(r.text)
    if responce_json[0]['gare'] == None:
        flag = False
    else:
        index  = index + 10
        gare = responce_json[0]['gare']
        for gara in gare:
            try:
                cig =""
                if gara.has_key('identificativo') and gara['identificativo'] != None:
                   
                   cig = gara['identificativo'].replace(".","")
                provenienza = 'ETRU'
                identificativo_gara = cig+'_'+provenienza
                
                oggetto =""
                if gara.has_key('oggettogara') and gara['oggettogara'] != None:
                   oggetto = removeNonAscii(gara['oggettogara'])
                   oggetto = oggetto.replace('"',' ')

                cat_prev =""
                tipologia = ""
                if gara.has_key('prevalente') and gara['prevalente'] != None:
                   cat_prev = gara['prevalente']
                   if cat_prev[:2] == 'OG' or cat_prev[:2] == 'OS':
                       tipologia = 'LAVORI'
                   else:
                       tipologia = 'SERVIZI'              

                procedura =""
                if gara.has_key('tipogara') and gara['tipogara'] != None:
                   procedura = gara['tipogara'].upper()



                ente =""
                if gara.has_key('ente') and gara['ente'] != None:
                   ente = removeNonAscii(gara['ente'])
                   ente = ente.replace('"',' ')
                #print ente

                   
                citta =""
                if gara.has_key('provincia') and gara['provincia'] != None:
                   citta = gara['provincia'].upper()

                   
                provincia =""
                if gara.has_key('siglaprov') and gara['siglaprov'] != None:
                   provincia = gara['siglaprov'].upper()


                regione =""
                if gara.has_key('regione') and gara['regione'] != None:
                   regione = gara['regione'].upper()

                
                importo =""
                if gara.has_key('importo') and gara['importo'] != None:
                   importo = gara['importo'].strip()
                   importo = prendi_import(importo)
                   
                d = dt.datetime.now()
                data_inserimento = d.strftime('%Y-%m-%d')
                

                data_pubblicazione =""
                if gara.has_key('riferimento') and gara['riferimento'] != None:
                   data_pubblicazione =  data_per_db(gara['riferimento'])

                data_scadenza =""
                if gara.has_key('scadenza') and gara['scadenza'] != None:
                   data_scadenza = data_per_db(gara['scadenza'])

                
                cpv =""
                if gara.has_key('cpv') and gara['cpv'] != None:
                   cpv = gara['cpv']


                categoria_prevalente =""
                if gara.has_key('prevalente') and gara['prevalente'] != None:
                   categoria_prevalente = gara['prevalente']

                
                categorie_scorp = []
                lista_scorp = []
                if gara.has_key('scorporabile') and gara['scorporabile'] != None:
                    lista_scorp = gara['scorporabile']
                if lista_scorp == None:
                    lista_scorp = []

                cat_scor1 =""
                if 0 <= 0 < len(lista_scorp):
                    cat_scor1 = lista_scorp[0]['cod']
                    categorie_scorp.append(cat_scor1)

                cat_scor2 =""
                if 0 <= 1 < len(lista_scorp):
                    cat_scor2 = lista_scorp[1]['cod']
                    categorie_scorp.append(cat_scor2)

                cat_scor3 =""
                if 0 <= 2 < len(lista_scorp):
                    cat_scor3 = lista_scorp[2]['cod']
                    categorie_scorp.append(cat_scor3)

                cat_scor4 =""
                if 0 <= 3 < len(lista_scorp):
                    cat_scor4 = lista_scorp[3]['cod']
                    categorie_scorp.append(cat_scor4)

                cat_scor5 =""
                if 0 <= 4 < len(lista_scorp):
                    cat_scor5 = lista_scorp[4]['cod']
                    categorie_scorp.append(cat_scor5)

                cat_scor6 =""
                if 0 <= 5 < len(lista_scorp):
                    cat_scor6 = lista_scorp[5]['cod']
                    categorie_scorp.append(cat_scor6)

                cat_scor7 =""
                if 0 <= 6 < len(lista_scorp):
                    cat_scor7 = lista_scorp[6]['cod']
                    categorie_scorp.append(cat_scor7)

                categorie_scorporabili_stringa = ""
                for una in categorie_scorp:
                        categorie_scorporabili_stringa = categorie_scorporabili_stringa + ','+ una
                categorie_scorporabili = categorie_scorporabili_stringa[1:]

                
                download = ''


                stringa_ricerca = oggetto +' '+ ente     
                bando_url =""

                # check se presente
                try:
                    sql_select ='SELECT * FROM gare.GARE_TUTTE where IDENTIFICATIVO_GARA ="'+identificativo_gara+'"'
                    cursore1 = conn.cursor()
                    cursore1.execute(sql_select)
                    presente = cursore1.fetchall()
                except:
                    #print "IDENTIFICATIVO ERRATO"
                    presente = 'ok'

                if presente:
                        #print identificativo_gara + " PRESENTE"
                        temp = 1
                else:

                        try:
                                # prende il link soo se presente
                                info_aggiuntive_dict =  {}
                                info_aggiuntive_dict['link'] = get_link(ente, citta)
                                info_aggiuntive = json.dumps(info_aggiuntive_dict)
                                print identificativo_gara+ " INSERITO"
                                insert_gara_etru(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
                        except:
                                print "ERRORE ETRU"
                                pass

            except Exception as e:
                s = str(removeNonAscii(str(e)))
                print s
                invia_mail("errore script ETRU"+testo, removeNonAscii(s))
                pass
                



       

