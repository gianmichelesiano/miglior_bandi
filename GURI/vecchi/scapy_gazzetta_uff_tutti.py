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
from HTMLParser import HTMLParser


conn= DBconnection.connection()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

              


def insert_gara_informagare(cig,oggetto,tipologia,procedura,ente,citta,provincia,regione,importo,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP):
                        cursore = conn.cursor()
                        sql = 'INSERT INTO gare.gare_informagare (cig,oggetto,tipologia,procedura,ente,citta,provincia,regione,importo,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP)   VALUES ("%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s")'% (cig,                                                
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
                        print sql
                                                                                           
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



# da cercare cig, tipologia gara, proceduna , citta





def converti_mese(str_mese):
    if str_mese[:3].lower() == "gen":
        return '01'
    if str_mese[:3].lower() == "feb":
        return '02'
    if str_mese[:3].lower() == "mar":
        return '03'
    if str_mese[:3].lower() == "apr":
        return '04'
    if str_mese[:3].lower() == "mag":
        return '04'
    if str_mese[:3].lower() == "giu":
        return '06'
    if str_mese[:3].lower() == "lug":
        return '07'
    if str_mese[:3].lower() == "ago":
        return '08'
    if str_mese[:3].lower() == "set":
        return '09'
    if str_mese[:3].lower() == "ott":
        return '10'
    if str_mese[:3].lower() == "nov":
        return '11'
    if str_mese[:3].lower() == "dic":
        return '12'


base_url = 'http://www.gazzettaufficiale.it/'
serviceurl_dettaglio = "http://www.gazzettaufficiale.it/atto/contratti/caricaDettaglioAtto/originario?atto.dataPubblicazioneGazzetta=2017-01-23&atto.codiceRedazionale=TU17BFC885"
serviceurl = "http://www.gazzettaufficiale.it/gazzetta/contratti/caricaDettaglio?dataPubblicazioneGazzetta=2017-01-11&numeroGazzetta=4&elenco30giorni=true"



r = requests.post(serviceurl)
testoHTML = r.text

soup = BeautifulSoup(testoHTML, "html.parser")
#print soup.text
risultati = soup.find_all("span", attrs={"class": "risultato"})
print len(risultati)

for risultato in risultati:

    mio =   risultato.a.get_text().strip().replace(chr(9),"").replace(chr(10),"")
    valori =  mio.split("(")
    
    ente = valori[0].strip()
    
    if len(valori)> 1:
        scadenza = valori[1].replace(')',"").replace('scad.','').strip().split(' ')
        if len(scadenza)>1:
            data_scadenza = scadenza[2]+'-'+converti_mese(scadenza[1])+'-'+scadenza[0]
            print data_scadenza


    link = base_url + risultato.a.get('href')
    print link
    print ente
    
    pagina = requests.post(link)
    testoHTML_pagina = pagina.text

    soup_pagina = BeautifulSoup(testoHTML_pagina, "html.parser")

    testo_intest = soup_pagina.find_all("h2", attrs={"class": "consultazione"})[0].get_text() 
    testo = soup_pagina.find_all("span", attrs={"class": "dettaglio_atto_testo_pc"}) 

    testo_per_parser = testo[0].get_text().replace('  ', ' ') + testo_intest



    # lista sezioni
    reg_sezioni = '[Ss]{1}[Ee]{1}[Zz]{1}[A-Za-z.]{0,4}[ ]{1}[IV123456]{1,2}'
    p = re.compile(reg_sezioni)
    print p.findall(testo_per_parser)

    # cap
    regex_cap = '[- ,][0-9]{5}[- .,;]'
    p = re.compile(regex_cap)
    print p.findall(testo_per_parser)

    # importo
    regex_importi = '[0-9.]{1,15}[,][0-9]+'
    p = re.compile(regex_importi)
    print p.findall(testo_per_parser)

    # mail
    regex_mail = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    p = re.compile(regex_mail)
    print p.findall(testo_per_parser)

    # sito www
    regex_sito_www = 'www.+[.][a-z]{2,3}'
    p = re.compile(regex_sito_www)
    print p.findall(testo_per_parser)

    # sito http
    regex_sito_http = 'http[s]*.+[.][a-z]{2}'
    p = re.compile(regex_sito_http)
    print p.findall(testo_per_parser)

    # date
    reg_data = '\d{1,2}[.-\/]{1,2}\d{1,2}[.-\/]{1,2}\d{2,4}'
    p = re.compile(reg_data)
    print p.findall(testo_per_parser)

    # date
    reg_CPV = '[- ,]\d{8}[- .,;]'
    p = re.compile(reg_CPV)
    print p.findall(testo_per_parser)

    # CIG
    regex_CIG = '[1-9]{2}[A-Z0-9]{8}'
    p = re.compile(regex_CIG)
    print p.findall(testo_per_parser)



    procedura = ''
    lista_procedura = ['APERTA', 'RISTRETTA', 'NEGOZIATA']
    if 'APERTA'  in testo_per_parser.upper():
        procedura = 'APERTA'
    if 'RISTRETTA'  in testo_per_parser.upper():
        procedura = 'RISTRETTA'
    if 'NEGOZIATA'  in testo_per_parser.upper():
        procedura = 'NEGOZIATA'

    print procedura

    tipologia = ''
    lista_procedura = ['LAVOR', 'SERVIZ', 'FORNITUR']
    if 'LAVOR'  in testo_per_parser.upper():
        tipologia = 'LAVORI'
    if 'RISTRETTA'  in testo_per_parser.upper():
        tipologia = 'SERVIZ'
    if 'NEGOZIATA'  in testo_per_parser.upper():
        tipologia = 'FORNITUR'

    print tipologia
    print "--------------------------"

#print testoHTML.split('<span class="dettaglio')[1].split('</body>')[0]



"""
SEZIONE I: AMMINISTRAZIONE AGGIUDICATRICE
SEZIONE II: OGGETTO DELL’APPALTO
SEZIONE III: INFORMAZIONI DI CARATTERE GIURIDICO, ECONOMICO, FINANZIARIO E TECNICO
SEZIONE IV: PROCEDURA.
SEZIONE V : (EVENTUALE).
SEZIONE VI : ALTRE INFORMAZIONI.
"""

tipo1 = 'SEZIONE I,SEZIONE II'

"""
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
        print iden
        cig = iden+'_INFOGARE'
        
        scadenza = celle[3].get_text()


        print data_per_db(scadenza.strip())
        data_scadenza = data_per_db(scadenza.strip())
        
        ente = celle[4].get_text().strip()
        print ente
            
        regione = celle[5].get_text().replace(',','').strip()
        print regione

        oggetto_tutti = celle[6].get_text().strip()
        info_oggetti = oggetto_tutti.split('.')

        oggetto = ''
        for info in info_oggetti:
            if len(info)>0:
                if info[0] != ' ':
                    if info[0] != '(':
                        oggetto = oggetto + info
                    
            
        
        #oggetto = info_oggetti[0]
        print oggetto
        #oggetto = info_oggetti[0]
        #print oggetto_tutti

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
            

        print "___"
        print cat_prev
        print "___"


        cat_scor1 = ''
        cat_scor2= ''
        cat_scor3= ''
        cat_scor4= ''
        cat_scor5= ''
        cat_scorps = celle[8].get_text().strip()
        print cat_scorps
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
             print str(procedura_dett).replace('<br/>',' ').replace('<strong><span align="left" class="grande_10">','').replace('</span></strong>','')
        print importo_fin


        
        procedura = str(celle[10]).replace('<br/>',' ').replace('<td>','').replace('</td>','').strip()
        print str(procedura).replace('<br/>',' ').replace('<td>','').replace('</td>','').strip()
        dettagli = celle[11].get_text()
        print dettagli

        


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
        insert_gara_informagare(cig,oggetto.upper(),tipologia.upper(),procedura.upper(),ente.upper(),citta.upper(),provincia.upper(),regione.upper(),importo_fin,data_pubblicazione,data_scadenza,cat_prev,cat_scor1,cat_scor2,cat_scor3,cat_scor4,cat_scor5,cpv,bando_url,bando_pdf,ribasso,criterio_agg,data_agg,importo_agg,nr_offerte,aggiudicatario,scaduto,data_inserimento, linkAVCP)
"""
