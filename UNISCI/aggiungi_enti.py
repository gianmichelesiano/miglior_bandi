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
import sys


import bs4
import time
from lxml import html





conn= DBconnection.connection()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))





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


def get_link(ente, citta):
        link = ''
        if 1:
                conn= DBconnection.connection()
                cursore = conn.cursor()
                sql_link = 'SELECT LINK FROM gare.LINK_ENTI where ente  = "'+ente+'"'
                #print sql_link
                
                cursore.execute(sql_link)
                data=cursore.fetchall()
                conn.close()
                print "+++"
                print len(data)
                print "+++"
                if len(data)>0:
                        link = data[0][0]
                else:
                        keywords = ente + " " + citta
                        risultati_duck = search_duckduckgo(keywords, max_results=1)
                        time.sleep(5)
                        for ris in risultati_duck:
                                link = ris

        return link




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


def cerca_con_yahoo(query):
        url = "http://search.yahoo.com/search?p=%s"
        r = requests.get(url % query) 
        soup = BeautifulSoup(r.text, "lxml")
        soup.find_all(attrs={"class": "yschttl"})
        res = []
        for link in soup.find_all(attrs={"class": "title"})[:5]:
                #print link.a['href']
                res.append(link.a['href'])
        return res


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



lista_da_eliminare = ['ulmon', 'maprika', 'pagepress', 'yahoo', 'google', 'wikipedia', 'pdf', 'halley', '4321property', 'gazzettaufficiale', 'paginebianche',
                      '1stcrib', 'twitter', 'facebook', 'keigai', 'familysearch', 'gazzettaufficiale', 'pageglance'
                      'italygen' ,'anyfiles', 'Who', 'who', 'gareeappalti', 'slideserve', 'bb30', 'academic', 'linkedin', 'triposo','italiabellezza']


curr = conn.cursor()

def insert__nuovo_ente(ente, link):
    conn= DBconnection.connection()
    curr_insert = conn.cursor()
    sql_insert = 'INSERT INTO gare.LINK_ENTI (ENTE, LINK) VALUES ("%s","%s")'% (ente, link)
    curr_insert.execute(sql_insert)
    conn.commit()
    conn.close()
    return 


def update_gare_tutte(info_aggiuntive, iden):
    conn= DBconnection.connection()
    curr_update = conn.cursor()
    sql_update = "UPDATE gare.GARE_TUTTE SET INFO_AGGIUNTIVE='%s' WHERE ID=%s " % (info_aggiuntive, iden)
    curr_update.execute (sql_update)
    conn.commit()
    conn.close()
    return

def update_gare_new(info_aggiuntive, iden):
    conn= DBconnection.connection()
    curr_update = conn.cursor()
    sql_update = "UPDATE gare.GARE_NEW SET INFO_AGGIUNTIVE='%s' WHERE ID=%s " % (info_aggiuntive, iden)
    curr_update.execute (sql_update)
    conn.commit()
    conn.close()
    return 

# GARE DA AGGIUNGERE SITO
sql_senza_sito = "SELECT * FROM gare.GARE_TUTTE where ENTE <> '' and (DOWNLOAD = '' and (INFO_AGGIUNTIVE = '{}' or INFO_AGGIUNTIVE = '{\"link\": \"\"}'))"
curr.execute(sql_senza_sito)
records = curr.fetchall()

for record in records:
    try:
        iden = record[0]
        ente = record[7].upper()
        citta = record[8].upper()
        print iden, ente, citta
        risultato_duck_duck = get_link(ente, citta)
        print "DUCK-DUCK"
        link = risultato_duck_duck
        print risultato_duck_duck
        if risultato_duck_duck == '' or any(word in risultato_duck_duck for word in lista_da_eliminare):
            keywords = ente +' '+ citta
            risultato_google = trova_con_google(keywords)
            print "google"
            print risultato_google
            link = risultato_google
            insert__nuovo_ente(ente, link)
            time.sleep(3)
        
        info_aggiuntive_dict =  {}
        info_aggiuntive_dict['link_trovato'] = link
        info_aggiuntive = json.dumps(info_aggiuntive_dict)
        try:
            update_gare_tutte(info_aggiuntive, iden)
            update_gare_new(info_aggiuntive, iden)
        except:
            print "ERRORE UPDATE"
            pass
        print "-----------------"
        time.sleep(3)
    except:
        pass


