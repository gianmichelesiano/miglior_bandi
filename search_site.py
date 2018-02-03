# -*- coding: utf-8 -*-

import requests
import bs4
import time
from lxml import html
from pws import Bing
from bs4 import BeautifulSoup


def trova_con_google(da_trovare):
        url = 'https://www.google.it/search?site=&q='+da_trovare
        print url
        r = requests.get(url)
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
                return result


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

keywords =  "MANIFESTAZIONE DI INTERESSE PER L’INDIVIDUAZIONE DEGLI OPERATORI ECONOMICI DA INVITARE ALLA PROCEDURA NEGOZIATA PER L’AFFIDAMENTO RELATIVO ALLA ESECUZIONE DELLE VERIFICHE PREVISTE DALLA NORMA CEI 64-8/7 NEI LOCALI ADIBITI AD"
risultati_google = trova_con_google(keywords)
for uno in risultati_google:
        print uno

"""        
keywords =  "comune di sarno"
#risultati_google =  trova_con_google(keywords)
for uno in risultati_google:
        print uno
risultati_duckduckgo =  search_duckduckgo(keywords, max_results=5)
for uno in risultati_duckduckgo:
        print uno
risultati_bing = Bing.search(keywords, 5)['results']
for uno in risultati_bing:
        print uno['link']

risultati_yahoo =  cervca_con_yahoo(keywords)
for uno in risultati_yahoo:
        print uno
"""

"""
keywords =  "MANIFESTAZIONE DI INTERESSE PER L’INDIVIDUAZIONE DEGLI OPERATORI ECONOMICI DA INVITARE ALLA PROCEDURA NEGOZIATA PER L’AFFIDAMENTO RELATIVO ALLA ESECUZIONE DELLE VERIFICHE PREVISTE DALLA NORMA CEI 64-8/7 NEI LOCALI ADIBITI AD"


risultati_google =  trova_con_google(keywords)
for uno in risultati_google:
        print uno
"""





"""

# salva pdf
risultato = 'http://www.aslcn2.it/media/2017/01/Determina-a-contrarreprotezionefulminidel25012017.pdf'
#url = 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf'
r = requests.get(risultato, stream=True)
with open('capocchia.pdf', 'wb') as f:
    f.write(r.content)

# legge pdf
import PyPDF2
pdfFileObj = open('capocchia.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print pdfReader

num_pagine = pdfReader.numPages

testo_tot = ""
for i in range(num_pagine):
        print i
        text_pag = pdfReader.getPage(i)
        testo_tot = testo_tot + text_pag.extractText()

print testo_tot
import re
regex_cap = '[- ,][0-9]{5}[- .,;]'
p = re.compile(regex_cap)
lista_cap =  p.findall(testo_tot)

print lista_cap

"""


