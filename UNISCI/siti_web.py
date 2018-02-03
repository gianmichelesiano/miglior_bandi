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
from lxml import html
import DBconnection
import bs4

# selezionare le gare new
# controllare se già esiste
# insert

def insert__nuovo_ente(ente, link):
    conn= DBconnection.connection()
    curr_insert = conn.cursor()
    sql_insert = 'INSERT INTO gare.LINK_ENTI (ENTE, LINK) VALUES ("%s","%s")'% (ente, link)
    curr_insert.execute(sql_insert)
    conn.commit()
    conn.close()
    return 


def trova_con_google(da_trovare):
        url = 'https://www.google.it/search?site=&q='+da_trovare
        try:
            r = requests.get(url)
        except:
            r = requests.get(unicode(url, errors='ignore'))
        responce =  r.text
        soup = bs4.BeautifulSoup(responce, "lxml")
        result = []
        for singolo in soup.find_all(attrs={"class": "g"}):
                #print singolo
                titolo = singolo.a.get_text()
                link =  singolo.a['href'].split('&sa=')[0].replace('/url?q=','')

                if link and titolo:
                        dicz = {}
                        dicz['titolo']=titolo
                        dicz['link']=link
                        result.append(dicz)
                #return result
                for uno in result:
                    return uno['link']

def search_duckduckgo(keywords, max_results=None):
	url = 'https://duckduckgo.com/html/'
	params = {
		'q': keywords,
		's': '0',
	}

	yielded = 0
	while True:
		res = requests.post(url, data=params)
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

def getHostName(url):
    import urlparse
    hostname = urlparse.urlparse(url).hostname
    if 'https://' in url:
        hostname =  'https://'+hostname
    if 'http://' in url:
        hostname =  'http://'+hostname
    return hostname


conn= DBconnection.connection()
curr = conn.cursor()


sql_comuni = "SELECT * FROM gare.comuni_abitanti;"
curr.execute(sql_comuni)
tutti_i_comuni = curr.fetchall()

i = 0
for comune in tutti_i_comuni:
    nome = comune[2]
    #print nome.upper()
    ricerca = 'COMUNE DI '+nome.upper()
    #print ricerca
    sql_new = 'SELECT * FROM gare.LINK_ENTI WHERE ente = "%s"'  % (ricerca)
    curr.execute(sql_new)
    enti_tutti = curr.fetchall()
    if len(enti_tutti) <1:
        
        risultati_duck = search_duckduckgo(ricerca, max_results=1)
        link = ''
        for ris in risultati_duck:
                link = ris
        if link != '':
            hostName= getHostName(link)
        else:
            hostName = 'NONTROVATO'
        if nome.lower() in hostName:
            print "Duck"
            print ricerca
            print hostName
            insert__nuovo_ente(ricerca, hostName)
            
        else:
            print "google"
            print ricerca
            print hostName
            hostName = trova_con_google(ricerca)
            print hostName
            insert__nuovo_ente(ricerca, hostName)

        i = i +1
        print  "----"
      
        
        time.sleep(1)
    
print i   
    





