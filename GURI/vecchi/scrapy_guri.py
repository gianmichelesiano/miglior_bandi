# -*- coding: utf-8 -*-

import MySQLdb
import urllib
import urllib2
import re
import string
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import datetime
import datetime as dt
import time
import requests
import pprint
import json
import sys
import DBconnection
from HTMLParser import HTMLParser
import DBconnection
conn= DBconnection.connection()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))


def  pulisci (parola):
    parola = re.sub(u"(\u2018|\u2019)", "'", parola)
    parola = re.sub(u"(\u201c|\u201d)", "'", parola)
    parola = re.sub(u"(\u0102)", "a'", parola)
    parola = re.sub(u"(\u0102\xa0)", "a'", parola)
    parola = re.sub(u"(\u0102\xa0)", "a'", parola)
    parola = re.sub(u"(\u0102\xb4)", "o'", parola)
    parola = re.sub(u"(\u0102\xa8)", "e'", parola)
    parola = re.sub(u"(\u2013)", " ", parola)
    parola = re.sub(u"(\u0102\u02db)", "o'", parola)
    parola = re.sub(u"(\xe2\x80\x9c|\\xe2\x80\x93)", "'", parola)
    parola = re.sub(u"(\u0102\u0160)", "e'", parola)
    parola = re.sub(u"(\u20ac)", " ", parola)
    parola = re.sub(u"(\u201a)", " ", parola)
    parola = re.sub(u"(\u2122)", "'", parola)
    parola = re.sub(u"(\u0164|\u0165)", "'", parola)
    parola = re.sub(u"(\xec)", "i'", parola)
    parola = re.sub(u"(u037e)", "", parola)


    return parola


dict_reg = {
    'VEN':'VENETO',
    'LOM':'LOMBARDIA',
    'TOS':'TOSCANA',
    'SAR':'SARDEGNA',
    'ABR':'ABRUZZO',
    'BAS':'BASILICATA',
    'SIC':'SICILIA',
    'PIE':'PIEMONTE',
    'VDA': "VALLE D'AOSTA",
    'CAM':'CAMPANIA',
    'PUG':'PUGLIA',
    'EMR':'EMILIA-ROMAGNA',
    'CAL':'CALABRIA',
    'LAZ':'LAZIO',
    'LIG':'LIGURIA',
    'UMB':'UMBRIA',
    'FVG':'FRIULI-VENEZIA GIULIA',
    'MOL':'MOLISE',
    'TAA':'TRENTINO-ALTO ADIGE',
    'MAR':'MARCHE',
    }

with open('comuni.json') as json_data:
    file_json = json.load(json_data)

def trova_geo(cap_da_trovare):
    
    trovato = False
    valori = []
    citta = ''
    prov = ''
    regione = ''
    for uno in file_json:
        if cap_da_trovare in uno['cap']:
            sql = "SELECT Comune,PROVINCIA, REGIONE FROM gare.comuni_abitanti where Istat  = "+ str(uno['codice'])
            cursore = conn.cursor()
            cursore.execute(sql)
            valori  =  cursore.fetchone()
            trovato = True
    if not trovato:    
        cap_da_trovare = cap_da_trovare[:3]+"xx"
        sql = "SELECT Comune,PROVINCIA, REGIONE FROM gare.comuni_abitanti where CAP  = '"+ str(cap_da_trovare)+"'"
        #print sql
        cursore = conn.cursor()
        cursore.execute(sql)
        valori  =  cursore.fetchone()
    if valori ==  None:
        valori = []

    if len(valori) > 2:
        citta = valori[0]
        prov  = valori[1]
        regione = dict_reg[valori[2]]
    return (removeNonAscii(citta), prov, regione)           


def insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        cursore = conn.cursor()
                        sql = """INSERT INTO gare.GARE_GURI(IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES ("%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s", "%s","%s",'%s','%s')"""% (identificativo_gara,
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
                        sql = pulisci (sql)
                 
                                                                                           
                        cursore.execute(sql)
                        conn.commit()





def prendi_import(imp):
    #imp = '€ 40.810.000'
    imp = removeNonAscii(imp)
    impor = imp.replace('.','').replace(' ','')
    return impor


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



def pulisci_oggetto(ingresso):
    ingresso = ingresso.replace("\n"," ").strip()
    ingresso = ingresso.replace(":","").strip()
    ingresso = ingresso.replace("1.1)","").strip()
    ingresso = ingresso.replace(".1.5)","").strip()
    ingresso = ingresso.replace("II.1.4)","").strip()
    ingresso = ingresso.replace("II.1)","").strip()
    
    ingresso = ingresso.replace("II.)","").strip()
    ingresso = ingresso.replace("II","").strip()
    ingresso = ingresso.replace(")","").strip()

    ingresso = ingresso.replace("II.1.1.","").strip()
    ingresso = ingresso.replace("OGGETTO DELL'APPALTO","").strip()
    ingresso = ingresso.replace("Oggetto dell'appalto","").strip()
    ingresso = ingresso.replace("Denominazione","").strip()
    ingresso = ingresso.replace("conferita","").strip()
    ingresso = ingresso.replace("all'appalto","").strip()
    ingresso = ingresso.replace("dall'amministrazione aggiudicatrice","").strip()
    
    ingresso = ingresso.replace("dall'ente aggiudicatore","").strip()
    ingresso = ingresso.replace("BREVE DESCRIZIONE","").strip()
    ingresso = ingresso.replace("DELL'APPALTO","").strip()
    ingresso = ingresso.replace("dell'appalto","").strip()      
    ingresso = ingresso.replace("OGGETTO","").strip()
    ingresso = ingresso.replace("Oggetto","").strip()
    ingresso = ingresso.replace("oggetto ","").strip()
    ingresso = ingresso.replace("DESCRIZIONE ","").strip()
    ingresso = ingresso.replace("Descrizione ","").strip()
    ingresso = ingresso.replace("Entita' ","").strip()
    ngresso = ingresso.replace("-"," ").strip()
    
    
    if len(ingresso) > 1:
        if ingresso[0] == '.':
            ingresso = ingresso[1:]
    if len(ingresso)>250:
        ingresso = ingresso[:200]+'...'
    return ingresso.strip()
    

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

base_url_tutti = 'http://www.gazzettaufficiale.it/30giorni/contratti;jsessionid=OlPY-HkISlMz1l8G2QExYg__.ntc-as4-guri2a'

reqeust = requests.get(base_url_tutti)
testoHTML = reqeust.text
soup = BeautifulSoup(testoHTML, "html.parser")

elementi_mesi = soup.find_all("div", attrs={"class": "elemento_mese"})

for elemento_mese in elementi_mesi:
            elemento = elemento_mese.find_all("span", attrs={"class": "titolo_atto"})[0]
            link = elemento.a['href']
            #print base_url+link

            data = link.split('ataPubblicazioneGazzetta=')[1].split('&numeroGazzetta')[0]
            #print data

            cursore = conn.cursor()
           
            sql = 'SELECT * FROM gare.GURI_FATTI;'
            cursore.execute(sql)
            records_fatti = cursore.fetchall()
            lista_fatti = []
            for uno in records_fatti:
                lista_fatti.append(uno[1])
            if data not in lista_fatti:
                print data
                #print "aggiungi gara"

                serviceurl = base_url+link
                
                # insert in tabella se non presente
                sql = 'INSERT INTO gare.GURI_FATTI (data) VALUES ("%s")'% (data)
                cursore.execute(sql)
                conn.commit()

                #AFFIUGE LE GARE

                provenienza = "GURI"

            
                r = requests.post(serviceurl)
                testoHTML = r.text

                soup = BeautifulSoup(testoHTML, "html.parser")
                #print soup.text
                risultati = soup.find_all("span", attrs={"class": "risultato"})


                for risultato in risultati:

                    mio =   risultato.a.get_text().strip().replace(chr(9),"").replace(chr(10),"")
                    valori =  mio.split("scad.")

                    ente = valori[0].replace('"',' ').replace('(',' ').strip()
                   

                    data_scadenza = ''
                    if len(valori)> 1:
                        scadenza = valori[1].replace(')',"").replace('scad.','').strip().split(' ')
                        if len(scadenza)>1:
                            if len(scadenza[0])==1:
                                giorno = "0"+scadenza[0]
                            else:
                                giorno = scadenza[0]
                            data_scadenza = scadenza[2]+'-'+converti_mese(scadenza[1])+'-'+giorno



                    link = base_url + risultato.a.get('href')
                    #print link
                    
                    
                    pagina = requests.post(link)
                    testoHTML_pagina = pagina.text

                    soup_pagina = BeautifulSoup(testoHTML_pagina, "html.parser")

                    testo_intest = soup_pagina.find_all("h2", attrs={"class": "consultazione"})[0].get_text() 
                    testo = soup_pagina.find_all("span", attrs={"class": "dettaglio_atto_testo_pc"}) 

                    testo_per_parser = testo[0].get_text().replace('  ', ' ') + testo_intest

                    # CIG
                    cig = ''
                    regex_CIG = '[1-9]{2}[A-Z0-9]{8}'
                    p = re.compile(regex_CIG)
                    if p.findall(testo_per_parser):
                        cig =  p.findall(testo_per_parser)[0].strip()
                        
                    identificativo_gara = cig +'_'+ provenienza
                    #print "CIG: ", cig
                    #print "IDENTIFICATIVO: ", identificativo_gara


                    # lista sezioni
                    oggetto = ''
                    reg_sezioni = '[Ss]{1}[Ee]{1}[Zz]{1}[A-Za-z.]{0,4}[ ]{1}[IV123456]{1,2}'
                    p = re.compile(reg_sezioni)
                    lista_sezioni =  p.findall(testo_per_parser)

                    if 'OGGETTO' in testo_per_parser.upper():
                        oggetto = testo_per_parser.upper().split('OGGETTO')[1]
                    if len(lista_sezioni)>3:
                        if "II" in lista_sezioni[1] or "2" in lista_sezioni[1] :
                            oggetto = testo_per_parser.split(lista_sezioni[1])[1].split(lista_sezioni[2])[0]

  
                                
                    
                    if oggetto != '' :
                        oggetto = oggetto.replace('-','',1)
                        oggetto = oggetto.replace('1','',3)
                        oggetto = oggetto.replace('.','',3)
                        oggetto =  pulisci_oggetto(oggetto).replace('"',' ').replace('  ',' ').strip()
                    else:
                        oggetto = "Dettagli nei link allegati"
                    #print  "OGGETTO:",  oggetto.upper()

                    tipologia = ''
                    lista_procedura = ['LAVOR', 'SERVIZ', 'FORNITUR']
                    if 'LAVOR'  in testo_per_parser.upper():
                        tipologia = 'LAVORI'
                    elif 'SERVIZ'  in testo_per_parser.upper():
                        tipologia = 'SERVIZI'
                    elif 'FORNITUR'  in testo_per_parser.upper():
                        tipologia = 'FORNITURE'

                    #print "TIPOLOGIA: ", tipologia



                    procedura = ''
                    lista_procedura = ['APERTA', 'RISTRETTA', 'NEGOZIATA']
                    if 'APERTA'  in testo_per_parser.upper():
                        procedura = 'PROCEDURA APERTA'
                    if 'RISTRETTA'  in testo_per_parser.upper():
                        procedura = 'PROCEDURA RISTRETTA'
                    if 'NEGOZIATA'  in testo_per_parser.upper():
                        procedura = 'PROCEDURA NEGOZIATA'

                    #print "PROCEDURA: ", procedura


                    # cap
                    regex_cap = '[- ,][0-9]{5}[- .,;]'
                    p = re.compile(regex_cap)
                    lista_cap =  p.findall(testo_per_parser)
                    if len(lista_cap)>0:
                        cap = lista_cap[0].replace('-','').replace('.','').strip()
                        
                        valori = trova_geo(cap)

                        citta = valori[0]
                        provincia = valori[1]
                        regione = valori[2]


                    # importo
                    regex_importi = '[0-9.]{3,15}[,][0-9]+'
                    p = re.compile(regex_importi)
                    list_importo =  p.findall(testo_per_parser)
                    importo = "N.D."
                    if len(list_importo):
                        importo = prendi_import(list_importo[0])
                    
                    #print "IMPORTO: ", importo

                    # CPV
                    cpv = ""
                    reg_CPV = '[ ,]\d{8}[- .,;]'
                    p = re.compile(reg_CPV)
                    CPV = p.findall(testo_per_parser)
                    if len(CPV) > 0:
                        cpv = CPV[0].replace(".","").replace(",","").replace("-","").replace(";","").strip()
                    #print "CPV:  ", cpv


                    lista_categorie = []
                    regex_categorie = 'OG[-0-9 ]{1,3}|OS[-0-9 ]{1,3}'
                    p = re.compile(regex_categorie)
                    lista_categorie =  p.findall(testo_per_parser)
                    #print "Lista categorie:  " , lista_categorie
                    categoria_prevalente = ''
                    for uno in lista_categorie:
                        categoria_prevalente = categoria_prevalente + uno.replace('-','').strip()+","
                    #print "categoria_prevalente:  " ,categoria_prevalente

                    dict_siti = {}
                    # mail
                    
                    regex_mail = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                    p = re.compile(regex_mail)
                    #print p.findall(testo_per_parser)
                    if len(p.findall(testo_per_parser))>0:
                        dict_siti['mail'] =  p.findall(testo_per_parser)[0].replace("'","")

                    # sito www
                    regex_sito_www = 'www.+[.][a-z]{2,3}'
                    p = re.compile(regex_sito_www)
                    
                    if len(p.findall(testo_per_parser))>0:
                        dict_siti['sito_www'] =  p.findall(testo_per_parser)[0].replace("'","")
                         

                    # sito http
                    regex_sito_http = 'http[s]*.+[.][a-z]{2}'
                    p = re.compile(regex_sito_http)
                    #print p.findall(testo_per_parser)
                    if len(p.findall(testo_per_parser))>0:
                        dict_siti['sito_www'] =  p.findall(testo_per_parser)[0].replace("'","")

                    dict_siti['sito_guri'] = link

                    

                    info_aggiuntive = json.dumps(dict_siti)
                        
                    # date
                    reg_data = '\d{1,2}[.-\/]{1,2}\d{1,2}[.-\/]{1,2}\d{2,4}'
                    p = re.compile(reg_data)
                    #print p.findall(testo_per_parser)
                    #print "lista_date  ", str(p.findall(testo_per_parser))


                    data_pubblicazione = 'N.D.'
                    categorie_scorporabili = ""

                    d = dt.datetime.now()
                    data_inserimento = d.strftime('%Y-%m-%d')

                    download = ''
                    
                    if data_scadenza != '':
                        try: 
                            insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
                        except:
                            pass
                    #print "---FINE GARA---"





    









