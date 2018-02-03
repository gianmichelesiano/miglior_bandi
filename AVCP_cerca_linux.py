# -*- coding: utf-8 -*-
import MySQLdb
import urllib
import urllib2
import re
import string
from bs4 import BeautifulSoup
import sys
import datetime
import calendar
import time
import cookielib
import webbrowser
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sys import platform as _platform



def trova_per_appalti(parser):
        cosa = re.compile(parser)
        lista=[]
        for match in cosa.finditer(descrizione):
                lista.append(match.group(0))
                return lista

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


account = get_session_info();
ip = get_server();
part_url = function_config();



 
def build_url(ogg_lotto,att_scad,pubb_da,pubb_a,categ):
     
    amministazione = ""
    aggiudicatario =""
    
    tipologia_appalto = "" # 1 lavori;2 servizi; 3 forniture
    settore = "" # 1 speciale ;2 ordinario;
    importo_da = ""
    importo_a = ""
    loc = "" # 1 localizz cosice istat
    cpv = ""
    crit_agg = ""  # 1 Massimo Ribasso ;2 Offerta economicamente più vantaggiosa;
    tipo_contr = ""
    proc = ""
    class_da = "" # da 1 a 8 se I a VIII
    class_a = "" # da 1 a 8 se I a VIII
   
    agg_da = "" # data aggiudicazionne da 01/01/1990
    agg_a = "" # data aggiudicazionne a 01/01/1990
    scad_da = "" # data scadenza da 01/01/1990
    scad_a = "" # data scadenza da 01/01/1990
    

    Stringa_url = "";
    Oggetto_lotto1 = ogg_lotto
    SA1 = amministazione
    OE1 = aggiudicatario
    att_scad1 = att_scad
    tipo_app1 = tipologia_appalto
    tipo_sett1 = settore
    importo_da1 = importo_da
    importo_a1 = importo_a
    loc1 = loc
    cpv1 = cpv;
    crit_agg1 = crit_agg
    tipo_contr1 = tipo_contr
    proc1 = proc
    class_da1 = class_da
    class_a1 = class_a
    pubb_da1 = pubb_da
    pubb_a1 = pubb_a
    agg_da1 = agg_da
    agg_a1 = agg_a
    scad_da1 = scad_da
    scad_a1 = scad_a
    categ1 = categ
    new_ogg = "";
    new_ogg = Oggetto_lotto1


    if( Oggetto_lotto1!=""):
        Stringa_url=new_ogg;
    else:
        Stringa_url="-100";
    if( SA1!=""):
        Stringa_url=Stringa_url+"^"+SA1;
    else:
        Stringa_url=Stringa_url+"^-100";
    if( OE1!=""):
        Stringa_url=Stringa_url+"^"+OE1;
    else:
        Stringa_url=Stringa_url+"^-100";
    if( tipo_app1!=""):
        Stringa_url=Stringa_url+"^"+tipo_app1;
    else:
        Stringa_url=Stringa_url+"^-100";
    if(tipo_sett1!=""):
        Stringa_url=Stringa_url+"^"+tipo_sett1;
    else:
        Stringa_url=Stringa_url+"^-100";
    if(importo_da1 !="" and importo_a1 !=""):
        Stringa_url=Stringa_url+"^"+importo_da1+"^"+importo_a1;
    else:
     if (importo_da1=="" and importo_a1 !=""):
        Stringa_url=Stringa_url+"^0^"+importo_a1;
     else:
      if (importo_a1=="" and importo_da1 !=""):
        Stringa_url=Stringa_url+"^"+importo_da1+"^9999999999999";
      else:
          Stringa_url=Stringa_url+"^-100^-100";
    if(loc1 !=""):
        Stringa_url=Stringa_url+"^"+loc1;
    else:
        Stringa_url=Stringa_url+"^-100";
    if(pubb_da1 !="" and pubb_a1 !=""):
     
     	Stringa_url=Stringa_url+"^"+pubb_da1+"^"+pubb_a1;
     
    elif (pubb_da1 =="" and pubb_a1 !=""):
        Stringa_url=Stringa_url+"^01/01/1800^"+pubb_a1;
    elif (pubb_da1 !="" and pubb_a1 ==""):
        Stringa_url=Stringa_url+"^"+pubb_da1+"^31/12/2099";
    else:
        Stringa_url=Stringa_url+"^01/01/1800^01/01/1800";


    if(agg_da1 !="" and agg_a1 !=""):
     	Stringa_url=Stringa_url+"^"+agg_da1+"^"+agg_a1;
     
    else:
     if(agg_da1 =="" and agg_a1 !=""):
         Stringa_url=Stringa_url+"^01/01/1800^"+agg_a1;
     else:
         if(agg_da1 !="" and agg_a1 ==""):
             Stringa_url=Stringa_url+"^"+agg_da1+"^31/12/2099";
         else:
            Stringa_url=Stringa_url+"^01/01/1800^01/01/1800";


    if(scad_da1 !="" and scad_a1 !=""):
        Stringa_url=Stringa_url+"^"+scad_da1+"^"+scad_a1;
    else:
        if(agg_da1 !="" and agg_a1 ==""):
            Stringa_url=Stringa_url+"^01/01/1800^"+scad_a1;
     
        else:
           if(scad_da1 !="" and scad_a1 ==""):
               Stringa_url=Stringa_url+"^"+scad_da1+"^31/12/2099";
     
           else:
                Stringa_url=Stringa_url+"^01/01/1800^01/01/1800";
    if( cpv1!=""):
        Stringa_url=Stringa_url+"^"+cpv1;
    else:
        Stringa_url=Stringa_url+"^-100";
    if( crit_agg1!=""):
        Stringa_url=Stringa_url+"^"+crit_agg1;
     
    else:
        Stringa_url=Stringa_url+"^-100";
    if( tipo_contr1!=""):
        Stringa_url=Stringa_url+"^"+tipo_contr1;
     
    else:
        Stringa_url=Stringa_url+"^-100";
    if( proc1!=""):
        Stringa_url=Stringa_url+"^"+proc1;
     
    else:
        Stringa_url=Stringa_url+"^-100";

    if(class_da1 !="" and class_a1 !="") :
        Stringa_url=Stringa_url+"^"+class_da1+"^"+class_a1;     
          
    else:
        Stringa_url=Stringa_url+"^-100^-100";
    if(categ1!=""):
        Stringa_url=Stringa_url+"^"+categ1;
     
    else:
        Stringa_url=Stringa_url+"^-100";
    if(att_scad1!=""):
        Stringa_url=Stringa_url+"^"+att_scad1;
     
    else:
        Stringa_url=Stringa_url+"^-100";


    return Stringa_url;

def quantiCIG(url_ricerca):

    headers = {
        'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
        'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'RedditTesting')]
    urllib2.install_opener(opener)
    
    
    formFields = (
    )

    # these have to be encoded    
    encodedFields = urllib.urlencode(formFields)

    req = urllib2.Request(url_ricerca, encodedFields)
    print "qu0"
    #time.sleep(20)
    f= urllib2.urlopen(req)
    time.sleep(20)
    soup1 = BeautifulSoup(f)
    testoSito  = soup1.get_text()
    stri="Maximum number of Server users exceeded"
    while stri in testoSito:
            print "errore pagina Numero massimo di utenti server superato"
            time.sleep(60)
            print "non apre"
            req = urllib2.Request(url_ricerca, encodedFields)
            f= urllib2.urlopen(req)
            soup1 = BeautifulSoup(f)
            testoSito  = soup1.get_text()
    
    parser_CIG = r'[0-9]{7}[A-Fa-f0-9]{3}'
    cosa = re.compile(parser_CIG)
    lista_CIG=[]
    for match in cosa.finditer(testoSito):
                lista_CIG.append(match.group(0))
        
        
    if len(lista_CIG)==2:
        
        pattern1 = r"a 300 record(.+)lotti"
        regex = re.compile(pattern1, re.IGNORECASE)
        nomec =re.search(regex, testoSito);
        quantiCIG =  nomec.group(1)
        quantiCIG = quantiCIG.replace(".","")
        quantiCIG = quantiCIG.replace(")","")
        quantiCIG = quantiCIG.replace("restituito","")
        quantiCIG = quantiCIG.replace("lotto","")
        quantiCIG = quantiCIG.replace(",","")
        quantiCIG = quantiCIG[1:].encode('utf-8').strip()
        if len(quantiCIG)<6:
                quantiCIG_int = int(quantiCIG)
                return quantiCIG_int
        
    if len(lista_CIG)==1:
                quantiCIG_int = 1
                return quantiCIG_int



def converti_data (data_py):
        data_ita = data_py.strftime('%d-%m-%Y')
        # cambia formato data se lavora su linux
        if _platform == "linux" or _platform == "linux2":
                data_ita = data_py.strftime('%m-%d-%Y')
        sitrng = str(data_ita)
        
        data_ita = sitrng.replace("-","/")
        return data_ita

def prendiCIG(url_ricerca):

    headers = {
        'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
        'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'RedditTesting')]
    urllib2.install_opener(opener)
    

    formFields = (
    )


    encodedFields = urllib.urlencode(formFields)

    req = urllib2.Request(url_ricerca, encodedFields, headers)
    f= urllib2.urlopen(req)
    
    f2=urllib2.urlopen(req)
    time.sleep(20)
    tutto =  f2.read()
    
    soup1 = BeautifulSoup(f)
    
    soup2 = str(soup1)
    #print "quo"
    testoSito  = soup1.get_text()
    #print "qua"
    stri="Maximum number of Server users exceeded"
    while stri in testoSito:
            print "errore pagina Numero massimo di utenti server superato"
            time.sleep(60)
            print "non apre"
            req = urllib2.Request(url_ricerca, encodedFields)
            f= urllib2.urlopen(req)
            soup1 = BeautifulSoup(f)
            testoSito  = soup1.get_text()
    
    parser_CIG = r'[0-9]{7}[A-Fa-f0-9]{3}'
    cosa = re.compile(parser_CIG)
    lista_CIG=[]
    for match in cosa.finditer(testoSito):
                print match.group(0)
                lista_CIG.append(match.group(0))
    return lista_CIG


parole = [ 
          "Lavori",     
          "Fornitura",
          "Servizi",
          "Servizio", 
          "Procedura",
          "Sistema",
          "Costruzione",
          "Gara",
          "Bando",
          "Progettazione",
          "Realizzazione",
          "Manutenzione",
          "Affidamento",
          "Convenzione",    
          "Interventi",
          "Intervento",
          "Lavoro",
          "Forniture",
          "Incarico",
          "Lotto",
          ]



percorso = os.getcwd()
path= percorso

#path_cvs = "C:/Users/Gianmichele/Downloads/Ricerca Export CSV.csv"
path_cvs = percorso.split('Google Drive')[0]+"/Downloads/Ricerca Export CSV.csv"
# cambia cartella se ubuntu
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    path_cvs = "/home/gio/Scaricati/Ricerca Export CSV.csv"   
    print path_cvs



file_nuovo = "/nuovo.txt"
print path+file_nuovo

#rimuove i file nuovo se ci sono
if os.path.exists(path+file_nuovo):
        print "dgfd"
        os.remove(path+file_nuovo)
else:
        print 'Non ce'


file_canc = "/recupero.txt"
print path+file_canc

#rimuove i file nuovo se ci sono
if os.path.exists(path+file_canc):
        print "dgfd"
        os.remove(path+file_canc)
else:
        print 'Non ce'


#rimuove i file gare da download
if os.path.exists(path_cvs):
        print "aaaaa"
        os.remove(path_cvs)
else:
        print 'Non ce in download'
        




lista_non_fatti  =[]
i=0
for i in range(1,2):
   for oggetto_lotto in parole:

        print oggetto_lotto
        fx = webdriver.FirefoxProfile()
        fx.set_preference("browser.download.manager.showWhenStarting", False)
        fx.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,text/csv,application/csv,application/octet-stream,text/comma-separated-values")
        br = webdriver.Firefox(firefox_profile=fx)

        categ = ""
        att_scad = str(i)
        print i
        Stringa = build_url(oggetto_lotto,att_scad,"","",categ)
        url_ricerca="http://"+ip+"/Microstrategy/asp/Main.aspx?evt=2048001&src=Main.aspx.2048001&visMode=0&hiddenSections=header,footer,path,dockTop&documentID=E1BCDDED4DB8F448D8B0349F96D12254&valuePromptAnswers="+Stringa+"&currentViewMedia=2&Main.aspx=-"+part_url+"&"+account
        print url_ricerca

        numeroCIG = 5
        if 1:
                lista_CIG = []
                print "1"
                br.get(url_ricerca)
                print "2"
                #time.sleep(5)
                try:
                        time.sleep(5)
                        br.find_element_by_link_text("Export in CSV").click()
                        print "2.1"
                except:
                        time.sleep(10)
                        br.find_element_by_link_text("Export in CSV").click()
                        print "2.2"
                print "3"
                """
                while not os.path.isfile(path_cvs):
                        print "aspetto"
                        time.sleep(1)
                        #f1 = open(path_cvs,"r")
                #else:
                """
                time.sleep(5)
                f1 = open(path_cvs,"r")

                Testo = f1.read()
                f1.close()
                Testo1  = Testo.replace(chr(0), "");
                parser_CIG = r'[0-9]{7}[A-Fa-f0-9]{3}'
                cosa = re.compile(parser_CIG)

                        
                os.remove(path_cvs)
                for match in cosa.finditer(Testo1):
                                cig  = match.group(0)
                                lista_CIG.append(cig)


                lista_CIG = list(set(lista_CIG))
                for cigo in lista_CIG:      
                        with open(path+file_nuovo, "a") as myfile:
                                                        
                                                        myfile.write(cigo+"\n\r")
                        

                print "completato"
                print "_______________________________________________________"
                br.quit()
 



fil = "/nuovo.txt"

print path+fil
f = open(path+fil,"r")
cigs = f.readlines()
lista_CIG = list(set(cigs))
f.close()


file_in = "/nuovo_pulito.txt"
if os.path.exists(path+file_in):
        print "dgfd"
        os.remove(path+file_in)
else:
        print 'Non ce'


for cigu in lista_CIG:
     cig = cigu.replace("\n"," ").replace("\r"," ").replace(' ', '')
     with open(path+file_in, "a") as myfile:
                                        myfile.write(cigu)







        
    

    
        





    

                            


