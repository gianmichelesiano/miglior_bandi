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




import DBconnection
conn= DBconnection.connection()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def convert_in_timestamp(data_stringa):
    if len(data_stringa)>9 and data_stringa != '1900-01-01':
        try:
            return time.mktime(dt.datetime.strptime(data_stringa, "%Y-%m-%d").timetuple())
        except:
            return 0 
    else:
        return 0 

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



def job():
    numero_mail_max = 5
    numero_mail = 0
    try:

        try:
            testo = "ANAC"
            execfile("ANAC//AVCP_cerca.py")
            print "FINITO CERCA ANAC"
            execfile("ANAC//insert_db.py")
            print "FINITO INSERT ANAC"
        except Exception as e:
            if numero_mail<numero_mail_max:
                s = str(removeNonAscii(str(e)))
                invia_mail("errore script "+testo, removeNonAscii(s))
                numero_mail = numero_mail + 1
                pass
            else:
                invia_mail("errore script SUPERATO NUMERO MAIL MAX", removeNonAscii(s))
                sys.exit()


        try:
            testo = "SCP"
            print "inizioSTP"
            execfile("SCP//nuovo_servizi_contratti.py")
            print "FINITO SCP"
        except Exception as e:
            if numero_mail<numero_mail_max:
                s = str(removeNonAscii(str(e)))
                invia_mail("errore script "+testo, removeNonAscii(s))
                numero_mail = numero_mail + 1
                pass
            else:
                invia_mail("errore script SUPERATO NUMERO MAIL MAX", removeNonAscii(s))
                sys.exit()


        try:
            testo = "GURI"
            execfile("GURI//scrapy_guri.py")
            print "FINITO GURI"
        except Exception as e:
            if numero_mail<numero_mail_max:
                s = str(removeNonAscii(str(e)))
                invia_mail("errore script "+testo, removeNonAscii(s))
                numero_mail = numero_mail + 1
                pass
            else:
                invia_mail("errore script SUPERATO NUMERO MAIL MAX", removeNonAscii(s))
                sys.exit()

        
        try:
            testo = "ETRURIA"
            execfile("ETRURIA//scrapy_etru.py")
            print "FINITO ETRURIA"
        except Exception as e:
            if numero_mail<numero_mail_max:
                s = str(removeNonAscii(str(e)))
                invia_mail("errore script "+testo, removeNonAscii(s))
                numero_mail = numero_mail + 1
                pass
            else:
                invia_mail("errore script SUPERATO NUMERO MAIL MAX", removeNonAscii(s))
                sys.exit()

        

        try:
            testo = "INFORMAGARE"
            execfile("INFORMAGARE//scapy_info.py")
            print "FINITO INFORMAGARE"
        except Exception as e:
            if numero_mail<numero_mail_max:
                s = str(removeNonAscii(str(e)))
                invia_mail("errore script "+testo, removeNonAscii(s))
                numero_mail = numero_mail + 1
                pass
            else:
                invia_mail("errore script SUPERATO NUMERO MAIL MAX", removeNonAscii(s))
                sys.exit()
        

        try:
            testo = "UNISCI NEW"
            execfile("UNISCI//merge_new.py")
            print "FINITO UNISCI"
            testo = "AGGIUNGI ENTI"
            execfile("UNISCI//aggiungi_enti.py")
            print "FINITO AGGIUNGI ENTI"

            testo = "FIREBASE"
            execfile("FIREBASE//firebase_add_new.py")
            print "FINITO FIREBASE"
            invia_mail("FINITO", "finito")
            print "MAIL INVIATA"

            testo = "INVIA PUSH"
            execfile("NOTIFICHE//push_ionic.py")
            print "PUSH INVIATA"
        except Exception as e:
            if numero_mail<numero_mail_max:
                s = str(removeNonAscii(str(e)))
                invia_mail("errore script "+testo, removeNonAscii(s))
                numero_mail = numero_mail + 1
                pass
            else:
                invia_mail("errore script SUPERATO NUMERO MAIL MAX", removeNonAscii(s))
                sys.exit()


    except Exception as e:
        s = str(removeNonAscii(str(e)))
        invia_mail("errore script "+testo, removeNonAscii(s))
        sys.exit()



    
schedule.every().day.at("09:18").do(job)


while 1:
    schedule.run_pending()
    time.sleep(1)
