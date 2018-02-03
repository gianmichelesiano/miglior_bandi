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

from difflib import SequenceMatcher

conn= DBconnection.connection()
cursore = conn.cursor()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


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


def calcola_metrica (ente, url):
        words = ente.split(' ')
        i = 0
        lista_eliminare = ['DI', 'COMUNE', 'PROVINCIA', 'REGIONE', 'ISTITUTO', 'DIREZIONE', 'SCUOLA' ]
        for word in words:
                if word not in lista_eliminare:
                        if word.lower() in url:
                                i = i + 1
        return i

def insert_home(ente, url):
        sql = 'INSERT INTO gare.HOME_ENTI (ENTE, HOME) VALUES ("%s","%s")'% (ente, url)
        cursore.execute(sql)
        conn.commit()


gia_presenti = []
sql_enti = """SELECT * FROM gare.amministrazioni_190 where id>8684"""
cursore = conn.cursor()
cursore.execute(sql_enti)
sql_enti_records = cursore.fetchall()

for rec in sql_enti_records:
    try:
        ente = rec[2]
        url = rec[4]        
        ente = removeNonAscii(ente.replace('"','').replace('  '," "))
        if 'http://' in url:       
                url = url.replace('http://','').split('/')[0]
                url = 'http://'+url
        if 'https://' in url:       
                url = url.replace('https://','').split('/')[0]
                url = 'https://'+url
        print rec[0]
        print ente
        print url

        nuovo_url = ''
        metrica_ini = calcola_metrica (ente, url)

        if metrica_ini > 0:
                nuovo_url = url
                insert_home(ente, nuovo_url)
        else:
                time.sleep(2)
                risultati_duck = search_duckduckgo(ente, 1)
                
                for ris in risultati_duck:
                        url_duck = ris

                metrica_duck = calcola_metrica (ente, url_duck)

                if metrica_duck > 0:
                        nuovo_url = url_duck
                        
                insert_home(ente, nuovo_url)                
        print nuovo_url
        print "----"
    except:
        print "ERRORE", rec
        pass

