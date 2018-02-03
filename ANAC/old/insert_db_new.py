# -*- coding: utf-8 -*-
import schedule
import time
import smtplib
import re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import MySQLdb
import urllib
import urllib2
import sys
import string
from bs4 import BeautifulSoup
from sys import platform as _platform

import random 
import calendar
import time
import os
import json 
import duckduckgo
import requests
import datetime
import calendar
import time
import os
import json as m_json
import requests
import time
from datetime import datetime
import datetime as dt
import calendar


from firebase import firebase
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


def converti_data (data_py):
        data_ita = data_py.strftime('%d-%m-%Y')
        sitrng = str(data_ita)
        return data_ita

def get_session_info():
	
			uid = "web";
			access_type= "no";
			info = "uid="+uid+"&pwd="+access_type;			
			return info;
account = get_session_info()

def function_config():
			 name_server = "10*.119*.128*.95";
			 name_project = "SISk*_Extranet";
			 directory = "Extranet";
			 url_din = ""+name_server+"."+name_project+".0_&shared=*-1.*-1.0.0.0&ftb=0.422541B24E28B69DC5DF858B20E67091.*0.8.0.0-8.18_268453447.*-1.1.*0&fb=0.422541B24E28B69DC5DF858B20E67091."+directory+".8.0.0-8.768.769.774.770.773.772.775.55.256.10.257.776.777_268453447.*-1.1.*0";
			 return url_din;
part_url = function_config()
def get_server():
			server_ip = "portaletrasparenza.avcp.it";
			return server_ip;

ip = get_server()

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





def estrai_numero(impor):
    imp=impor.replace(",","")
    parser="\d+"
    cosa = re.compile(parser)
    lista=[]
    for match in cosa.finditer(imp):
                lista.append(match.group(0))
                if len(lista)!=0:
                        return lista[0]
from sys import platform as _platform
def prendi_import(imp):
    imp = removeNonAscii(imp)
    imp = imp.replace(u'\u0179',"")
    if _platform == "linux" or _platform == "linux2":
        impor = imp.replace(',','').replace(' ','')
        val = impor.split(".")
    else:
        impor = imp.replace('.','').replace(' ','')
        val = impor.split(",")
                
    #print imp

    if len(val) > 1:
        decimale = val[1][:2]
    else:
        decimale = "00"
    tot = val[0] +','+ decimale
    return tot

def estrai_OG(cat):
    grafo_cat = {
    'Edifici civili e industriali':'OG1',
    'Restauro e manutenzione dei beni immobili sottoposti a tutela':'OG2',
    'Strade, autostrade, ponti, viadotti, ferrovie, metropolitane':'OG3',
    'Opere d’arte nel sottosuolo':'OG4',
    'Dighe':'OG5',
    'Acquedotti, gasdotti , oleodotti, opere di irrigazione e di evacuazione':'OG6',
    'Acquedotti, gasdotti, oleodotti, opere di irrigazione e di evacuazione':'OG6',
    'Opere marittime e lavori di dragaggio':'OG7',
    'Opere fluviali, di difesa, di sistemazione idraulica e di bonifica':'OG8',
    'Impianti per la produzione di energia elettrica':'OG9',
    'Impianti per la trasformazione alta/media tensione e e per la distribuzione di energia elettrica in corrente alternata e continua ed impianti di pubblica illuminazione':'OG10',
    'Impianti tecnologici':'OG11',
    'Opere ed impianti di bonifica e protezione ambientale':'OG12',
    'Opere di ingegneria naturalistica':'OG13',
    'Lavori in terra':'OS1',
    'Superfici decorate di beni immobili del patrimonio culturale e beni culturali mobili di interesse storico, artistico, archeologico ed etnoantropologico':'OS2-A',
    'Beni culturali mobili di interesse archivistico e librario':'OS2-B',
    'Impianti idrico-sanitario, cucine, lavanderie':'OS3',
    'Impianti elettromeccanici trasportatori':'OS4',
    'Impianti pneumatici e antintrusione':'OS5',
    'Finiture di opere generali in materiali lignei, plastici, metallici e vetrosi':'OS6',
    'Finiture di opere generali di natura edile':'OS7',
    'Opere di impermeabilizzazione':'OS8',
    'Impianti per la segnaletica luminosa e la sicurezza del traffico':'OS9',
    'Segnaletica stradale non luminosa':'OS10',
    'Apparecchiature strutturali speciali':'OS11',
    'Barriere stradali di sicurezza':'OS12-A',
    'Barriere paramassi, fermaneve e simili':'OS12-B',
    'Strutture prefabbricate in cemento armato':'OS13',
    'Impianti di smaltimento e recupero dei rifiuti':'OS14',
    'Pulizie di acque marine, lacustri, fluviali':'OS15',
    'Impianti per centrali di produzione energia elettrica':'OS16',
    'Linee telefoniche ed impianti di telefonia':'OS17',
    'Componenti strutturali in acciaio':'OS18-A',
    'Componenti per facciate continue':'OS18-B',
    'Impianti di reti di telecomunicazione e di trasmissione dati':'OS19',
    'Rilevamenti topografici':'OS20-A',
    'Indagini geognostiche':'OS20-B',
    'Opere strutturali speciali':'OS21',
    'Impianti di potabilizzazione e depurazione':'OS22',
    'Demolizione di opere':'OS23',
    'Verde e arredo urbano':'OS24',
    'Scavi archeologici':'OS25',
    'Pavimentazioni e sovrastrutture speciali':'OS26',
    'Impianti per la trazione elettrica':'OS27',
    'Impianti termici e di condizionamento':'OS28',
    'Armamento ferroviario':'OS29',
    'Impianti interni elettrici, telefonici, radiotelefonici e televisivi':'OS30',
    'Impianti per la mobilità sospesa':'OS31',
    'Strutture in legno':'OS32',
    'Coperture speciali':'OS33',
    'Sistemi antirumore per infrastrutture di mobilità':'OS34',
    'Interventi a basso impatto ambientale':'OS35',

    }


    cat = cat.rstrip().lstrip()
    if cat.capitalize() in grafo_cat.keys():

        return grafo_cat.get(cat.capitalize())
    else:
        return ""

                
def insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download):
                        cursore = conn.cursor()
                        sql = """INSERT INTO gare.GARE_ANAC (IDENTIFICATIVO_GARA, PROVENIENZA, CIG, OGGETTO, TIPOLOGIA, PROCEDURA, ENTE, CITTA, PROVINCIA, REGIONE, IMPORTO, DATA_INSERIMENTO, DATA_PUBBLICAZIONE, DATA_SCADENZA, CPV, CATEGORIA_PREVALENTE, CATEGORIE_SCORPORABILI, INFO_AGGIUNTIVE ,DOWNLOAD)   VALUES ("%s","%s", "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s",'%s')"""% (identificativo_gara,
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

#insert_gara("identificativo_gara", "provenienza", "cig", "oggetto", "tipologia", "procedura", "ente", "citta", "provincia", "regione", "importo", "data_inserimento", "data_pubblicazione", "data_scadenza", "cpv", "categoria_prevalente", "categorie_scorporabili", "info_aggiuntive", "download")


#ecco
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}


formFields = (
)

percorso = os.getcwd()

path= percorso

fil = "/nuovo_pulito.txt"

f = open(path+fil,"r")
cigs = f.readlines()
lista_CIG = list(set(cigs))
f.close()


#cigs = ['692174008C']


for cigu in cigs:
        try:
            cig = cigu.replace("\n"," ").replace("\r"," ").replace(' ', '')
            

            sql_select ='SELECT CIG FROM gare.GARE_TUTTE where CIG="'+cig+'"'
            cursore1 = conn.cursor()
            cursore1.execute(sql_select)
            cig_pres = cursore1.fetchall()

            if cig_pres:
                    #print cig + " PRESENTE"
                    with open(path+"/presenti.txt", "a") as myfile:
                                        myfile.write(cig+"\n\r")
            else:
                    #print cig + " AGGIUNTO"
                    url_CIG = "http://"+ip+"/Microstrategy/asp/Main.aspx?evt=2048001&src=Main.aspx.2048001&visMode=0&hiddenSections=header,footer,path,dockTop&documentID=0E392EF94E86CCDD246176A3580200AB&valuePromptAnswers="+cig+"&currentViewMedia=2&Main.aspx=-"+part_url+"&"+account;
                    encodedFields = urllib.urlencode(formFields)

                    driver = webdriver.Firefox()
                    driver.get(url_CIG)
                    time.sleep(5)
                    f = driver.page_source
                    
                    if os.path.exists('page_content.html'):
                            os.remove('page_content.html')


                    with open('page_content.html', 'w') as fid:
                            fid.write(removeNonAscii(f))
                            
                    txt = open('page_content.html')
                    
                    f = txt.read()
                    txt.close()

                    
                    soup1 = BeautifulSoup(f)
                    testo=soup1.get_text()
                   
                    driver.quit()
                
                    stri="Maximum number of Server users exceeded"
                    while stri in testo:
                            time.sleep(15)
                            req = urllib2.Request(url_CIG, encodedFields)
                            f= urllib2.urlopen(req)
                            soup1 = BeautifulSoup(f)
                            testo  = soup1.get_text()
            
                    anagrafica = []

                    for link in soup1.find_all(class_="r-h"):
                        for link_t in link.find_all('td'):
                            
                            elem=link_t.get_text()
                            anagrafica.append(elem)
                        else:
                            anagrafica.append("")

                    if anagrafica:

                            """
                            "identificativo_gara", "provenienza", "cig", "oggetto", "tipologia", "procedura", "ente", "citta", "provincia", "regione", "importo", "data_inserimento", "data_pubblicazione", "data_scadenza", "cpv", "categoria_prevalente", "categorie_scorporabili", "info_aggiuntive", "download"
                            """
                            cig = anagrafica[36]

                            provenienza = "ANAC"
                            identificativo_gara = cig+"_"+provenienza

                            og = anagrafica[4] 
                            oggetto = og[0:250].replace('"',"'")

                            tipologia = anagrafica[51]

                            procedura = anagrafica[13]

                            ente = anagrafica[27].replace('"',"'")

                            citta=str(anagrafica[24])
                            if citta == "ND":
                                citta=str(anagrafica[54])
                                
                            provincia=prendi_provincia_regione2 (citta)[0]

                            regione = prendi_provincia_regione2 (citta)[1].upper()

                            importo =prendi_import(anagrafica[45])

                            d = dt.datetime.now()
                            data_inserimento = d.strftime('%Y-%m-%d')

                            data_pubblicazione = ""
                            for link in soup1.find_all(class_="r-c13_K255"):
                                if link.get_text():  
                                         data_pubblicazione= link.get_text()
                                         data_pubblicazione= data_per_db(data_pubblicazione)
                                         
                                         
                            data_scadenza = data_per_db(anagrafica[42])

                            cpv = anagrafica[63]

                            categoria_prevalente = estrai_OG(anagrafica[60])

                            categorie_scorp = []
                            for link in soup1.find_all(class_="r-c12_K160"):
                                 OG = estrai_OG(link.get_text())
                                 if OG:
                                     categorie_scorp.append(OG)
                            for link in soup1.find_all(class_="r-c13_K160"):
                                 OG = estrai_OG(link.get_text())
                                 if OG:
                                     categorie_scorp.append(OG)
                            categorie_scorporabili_stringa = ""
                            for una in categorie_scorp:
                                categorie_scorporabili_stringa = categorie_scorporabili_stringa + ','+ una
                            categorie_scorporabili = categorie_scorporabili_stringa



                            info_aggiuntive = ""
                            
                            bandi = []
                            for link in soup1.find_all(class_="r-c16_K255"):
                                if link.get_text():
                                    for link1 in link.find_all('a'):
                                        bando_autor = link1.get('href')
                                        bandi.append(bando_autor)
                    
                            for link in soup1.find_all(class_="r-c14_K255"):
                                if link.get_text():
                                    for link1 in link.find_all('a'):
                                        bando_autor = link1.get('href')
                                        bandi.append(bando_autor)
                            b=0
                            bando_url1 = ""
                            bando_pdf1 = ""
                            while b < len(bandi):
                                indice = str(b)
                                stri=indice + ":" + bandi[b]
                                if "pdf" in bandi[b]:
                                    bando_pdf1 = bandi[b]
                                   
                                else:
                                    bando_url1 = bandi[b]
                                b = b + 1

                            download = json.dumps({'url':bando_url1, 'pdf':bando_pdf1, 'anac':url_CIG})
                            
                            #print identificativo_gara
                            insert_gara(identificativo_gara, provenienza, cig, oggetto, tipologia, procedura, ente, citta, provincia, regione, importo, data_inserimento, data_pubblicazione, data_scadenza, cpv, categoria_prevalente, categorie_scorporabili, info_aggiuntive, download)
                            
  
        except Exception as e:
                s = str(removeNonAscii(str(e)))
                #invia_mail("errore script ANAC", removeNonAscii(s))
                print s
                pass
                            
                                
                            
                                    
                            

                            




