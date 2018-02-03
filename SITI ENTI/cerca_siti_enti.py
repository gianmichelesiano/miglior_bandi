# -*- coding: utf-8 -*-

import requests
import bs4
import time
from lxml import html

from bs4 import BeautifulSoup
import time
from random import randint

import DBconnection
conn= DBconnection.connection()
cursore = conn.cursor()
import sys

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



# TUTTI 
sql_enti = 'SELECT * from  gare.indirizzi_amministrazioni_190 where id >26509 ;'
cursore = conn.cursor()
cursore.execute(sql_enti)
records_enti_190_tutti = cursore.fetchall()
lista_enti_tutti= []
for uno in records_enti_190_tutti:
        if "COMUNE" in uno[2] or "PROVI" in uno[2] or "REGIONE" in uno[2]:
                lista_enti_tutti.append((uno[2],uno[0]))






gia_presenti = []
sql_gia_presenti = 'SELECT * FROM gare.LINK_ENTI;'
cursore = conn.cursor()
cursore.execute(sql_gia_presenti)
gia_presenti_records = cursore.fetchall()
for record in gia_presenti_records:
        gia_presenti.append(record[1])


x = 0
tempo_stop = randint(0,5)
for ente_rec in lista_enti_tutti:
        ente = ente_rec[0]
        if ente not in gia_presenti:
                keywords = ente + " GARE"
                link = ''
                risultati_duck = search_duckduckgo(keywords, max_results=1)
                for ris in risultati_duck:
                         link = ris

                time.sleep(tempo_stop)
                
                if link != '':
                        print ente
                        print link
                        print "---"
                        sql = 'INSERT INTO gare.LINK_ENTI (ENTE, LINK) VALUES ("%s","%s")'% (ente, link)
                        cursore.execute(sql)
                        conn.commit()
                else:
                        x = x + 1
                        print "USCITA FORZATA"
                        print 'ID', ente_rec
                        time.sleep(300)
                        if x>5:
                                sys.exit()
                        

