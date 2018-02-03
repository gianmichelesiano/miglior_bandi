# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import datetime as dt
import json

import smtplib
import re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import DBconnection

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


def  pulisci(parola):
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
    parola = re.sub(u"(\u02db)", "", parola)
    parola = re.sub(u"(\u0160)", "", parola)

    parola = re.sub(u"(\u0164|\u0165)", "'", parola)
    
    

    return parola
                    
     

    
    return parola
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def pulisci_gara(gara):
    gara_pulita = []
    for una in gara:
        if type(una) == str:
            gara_pulita.append(removeNonAscii(str(una)))
        else:
            gara_pulita.append(una)
    return gara_pulita

def prendi_import(imp):
    #imp = '€ 40.810.000'
    imp = imp.replace(u'\u20ac',"")
    
    imp = imp.replace(u'\u0179',"")
    impor = imp.replace('.','').replace(' ','')
    val = impor.split(",")

    if len(val) > 1:
        decimale = val[1][:2]
    else:
        decimale = "00"
    tot = val[0] +','+ decimale
    return tot

def data_per_db(data):
    data=data.replace(u'\xa0', '')
    if data:               
        d = datetime.strptime(data, '%d/%m/%Y')
        day_string = d.strftime('%Y-%m-%d')
        
    else:
        day_string = "1900-01-01"
    return day_string

def prendi_provincia_regione2(comun):
    try:
        sql_com = 'SELECT * FROM gare.comuni where nome = "'+comun+'"'
        cursore1 = conn.cursor()
        cursore1.execute(sql_com)
        id_prov  = cursore1.fetchall()[0][2]   
        sql_prov   = 'SELECT * FROM gare.province where id = '+ str(id_prov)
        cursore1.execute(sql_prov)
        prov =  cursore1.fetchall()

        provincia = prov[0][1]
        sql_sigle = 'SELECT * FROM gare.province_sigle where nomeprovincia = "'+provincia+'"'
        cursore1.execute(sql_sigle)
        
        try:
            sigla_prov   =  cursore1.fetchall()[0][3].replace('\xe9','')
        except:
            sigla_prov =  provincia.replace('\xe9','')
        
        id_regione = prov[0][2]
        sql_reg   = 'SELECT * FROM gare.regioni where id = '+ str(id_regione)
        cursore1.execute(sql_reg)
        regione  =  cursore1.fetchall()[0][1].replace('\xe9','')
        
    except:
        sigla_prov = ''
        regione = ''
    return (removeNonAscii(sigla_prov),removeNonAscii(regione))

def insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        conn_insert= DBconnection.connection()
                        cursore_insert = conn_insert.cursor()
                        sql = """INSERT INTO gare.GARE_SCP (IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES (%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)"""
                        
                        
                        cursore_insert.execute(sql, (identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download))                                                                   
                        
                        conn_insert.commit()
                        conn_insert.close()


base_url = "https://www.serviziocontrattipubblici.it"


tipologie = ["Lavori", "Servizi", "Forniture"]
provincie = ["AGRIGENTO", "ALESSANDRIA", "ANCONA", "AOSTA", "AREZZO", "ASCOLI PICENO", "ASTI", "AVELLINO", "BARI", "BARLETTA-ANDRIA-TRANI", "BELLUNO", "BENEVENTO", "BERGAMO", "BIELLA", "BOLOGNA", "BOLZANO", "BRESCIA", "BRINDISI", "CAGLIARI", "CALTANISSETTA", "CAMPOBASSO", "CARBONIA-IGLESIAS", "CASERTA", "CATANIA", "CATANZARO", "CHIETI", "COMO", "COSENZA", "CREMONA", "CROTONE", "CUNEO", "ENNA", "FERMO", "FERRARA", "FIRENZE", "FOGGIA", "FORLI CESENA", "FROSINONE", "GENOVA", "GORIZIA", "GROSSETO", "IMPERIA", "ISERNIA", "L'AQUILA", "LA SPEZIA", "LATINA", "LECCE", "LECCO", "LIVORNO", "LODI", "LUCCA", "MACERATA", "MANTOVA", "MASSA-CARRARA", "MATERA", "MEDIO CAMPIDANO", "MESSINA", "MILANO", "MODENA", "MONZA BRIANZA", "NAPOLI", "NOVARA", "NUORO", "OGLIASTRA", "OLBIA-TEMPIO PAUSANIA", "ORISTANO", "PADOVA", "PALERMO", "PARMA", "PAVIA", "PERUGIA", "PESARO E URBINO", "PESCARA", "PIACENZA", "PISA", "PISTOIA", "PORDENONE", "POTENZA", "PRATO", "RAGUSA", "RAVENNA", "REGGIO CALABRIA", "REGGIO EMILIA", "RIETI", "RIMINI", "ROMA", "ROVIGO", "SALERNO", "SASSARI", "SAVONA", "SIENA", "SIRACUSA", "SONDRIO", "TARANTO", "TERAMO", "TERNI", "TORINO", "TRAPANI", "TRENTO", "TREVISO", "TRIESTE", "UDINE", "VARESE", "VENEZIA", "VERBANIA", "VERCELLI", "VERONA", "VIBO VALENTIA", "VICENZA", "VITERBO"]
#provincie = ["VERCELLI", "VERONA", "VIBO VALENTIA", "VICENZA", "VITERBO"]

#prov = provincie[2]

url_ricerca = base_url+"/PubbAvvisiBandiEsiti/InitTrovaBandi.do"

for prov in provincie:
    for tipologia in tipologie:
        try:
            conn= DBconnection.connection()
            #print prov, tipologia

            br = webdriver.Firefox()
            br.get(url_ricerca)
            Select(br.find_element_by_name("provinciaSA")).select_by_visible_text(prov)
            Select(br.find_element_by_name("tipoBando")).select_by_visible_text(tipologia)
            br.find_element_by_css_selector("button[type=\"submit\"]").click()
            time.sleep(1)
            f = br.page_source
            soup = BeautifulSoup(f)
            gare = soup.find_all("ul", attrs={"class": "link_plus_no_indent"})
            br.quit()

            for gara in gare:
                # VALORI DALLA PAGINA RICERCA
                valori = gara.find_all('b')
                link_dettaglio = gara.li.a.get('href')
                oggetto_prima = valori[0].get_text()
                identificativo = valori[1].get_text()
                importo = valori[2].get_text()
                importo = prendi_import(importo)
                data_pubblicazione =  data_per_db(valori[3].get_text())
                data_scadenza = data_per_db(valori[4].get_text())


                #VALORI DALLA PAGINA DETTAGLIO
                if 1:
                    r = requests.get(base_url+link_dettaglio , timeout=5)
                    responce = r.content
                    soup_dettaglio = BeautifulSoup(responce)

                    box = soup_dettaglio.find_all("div", attrs={"class": "padding_box"})
                    righe = str(box[0]).split('<br/>')
                    lista_scorporabile = []
                    for riga in righe:
                        soup_contenuto = BeautifulSoup(riga).get_text().strip()

                        provenienza = 'SCP'
                        if 'CIG:' in soup_contenuto:
                            cig = soup_contenuto.split(':')[1].strip()
                            identificativo_gara = cig +'_'+provenienza
                        if 'Descrizione' in soup_contenuto:
                            oggetto = soup_contenuto.split(':')[1].strip().replace('"',"'")
                            oggetto = pulisci(oggetto)

                            

                        if 'Procedura' in soup_contenuto:
                            procedura = soup_contenuto.split(':')[1].strip().replace('"',"'")

                        if 'Denominazione' in soup_contenuto:
                            ente = soup_contenuto.split(':')[1].strip().replace('"',"'")
                            ente = pulisci (ente)

                        if 'Luogo ' in soup_contenuto:
                            citta = soup_contenuto.split(':')[1].strip()


                            provincia=prendi_provincia_regione2 (citta)[0]
                            if provincia == '':
                                if citta == '':
                                    citta = prov
                                provincia = prendi_provincia_regione2 (prov)[0]
                                
                            regione = prendi_provincia_regione2 (citta)[1].upper()
                            if regione == '':
                                regione = prendi_provincia_regione2 (prov)[1].upper()

                        if 'Importo del lotto' in soup_contenuto:
                            imp = soup_contenuto.split(':')[1].strip()
                            importo = prendi_import(imp)

                        d = dt.datetime.now()
                        data_inserimento = d.strftime('%Y-%m-%d')
                        #cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download

                        if 'CPV1' in soup_contenuto:
                            cpv = soup_contenuto.split(':')[1].strip()

                        if 'prevalente' in soup_contenuto:
                            categoria_prevalente = soup_contenuto.split(':')[1].split('-')[0].strip()
                        
                        if 'scorporabile' in soup_contenuto:
                            lista = soup_contenuto.split('scorporabile')
                            for uno in lista:
                                if ':' in uno:
                                    cat_scorp = uno.split(':')[1].split('-')[0].strip()
                                    lista_scorporabile.append(cat_scorp)
                        categorie_scorporabili = ','.join(lista_scorporabile)
                        
                        info_aggiuntive = ''

                    dict_link = {}
                    links = soup_dettaglio.find_all("ul", attrs={"class": "link_plus_no_indent"})
                    for link in links:
                        if 'href' in str(link):
                            valore =  base_url+link.a.get('href')
                            key =  link.a.get_text().strip()
                            if 'Bando' in key:
                                key = 'Bando di gara'
                            if 'Disciplinare' in key:
                                key = 'Disciplinare di gara'
                            if 'fascicolo' in key:
                                key = 'fascicolo'
                            dict_link [key] = valore
                            
                    download = json.dumps(dict_link)
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
                            temp =1
                    else:
                        try:
                            #print identificativo_gara + " AGGIUNTO"
                            insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia.upper(), procedura.upper(), ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
                        except:

                            
                            identificativo_gara = removeNonAscii(identificativo_gara)
                            provenienza = removeNonAscii(provenienza)
                            cig = removeNonAscii(cig)
                            oggetto = removeNonAscii(oggetto)
                            tipologia = removeNonAscii(tipologia)
                            procedura = removeNonAscii(procedura)
                            ente = removeNonAscii(ente)
                            citta = removeNonAscii(citta)
                            provincia = removeNonAscii(provincia)
                            regione = removeNonAscii(regione)
                            
                            cpv = removeNonAscii(cpv)
                            categoria_prevalente = removeNonAscii(categoria_prevalente)
                            categorie_scorporabili = removeNonAscii(categorie_scorporabili)
                            info_aggiuntive = removeNonAscii(info_aggiuntive)
                            download = removeNonAscii(download)

                            
                            #print identificativo_gara + " AGGIUNTO EXCEPT"
                            insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia.upper(), procedura.upper(), ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)

        except Exception as e:
                s = str(removeNonAscii(str(e)))
                print s
                #invia_mail("errore script SCP"+testo, removeNonAscii(s))
                pass
