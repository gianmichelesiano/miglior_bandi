import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


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


# ANAC
try:
    testo = "ANAC"
    execfile("ANAC//AVCP_cerca.py")
    print "FINITO CERCA ANAC"
    execfile("ANAC//insert_db.py")
    print "FINITO INSERT ANAC"
    testo = "SCP"
    execfile("SCP//nuovo_servizi_contratti.py")
    print "FINITO SCP"
    testo = "GURI"
    execfile("GURI//scrapy_guri.py")
    print "FINITO GURI"
    testo = "ETRURIA"
    execfile("ETRURIA//scrapy_etru.py")
    print "FINITO ETRURIA"
    testo = "INFORMAGARE"
    execfile("INFORMAGARE//scapy_info.py")
    print "FINITO INFORMAGARE"
    testo = "UNISCI"
    execfile("UNISCI//merge.py")
    print "FINITO UNISCI"
    testo = "FIREBASE"
    execfile("FIREBASE//firebase_add.py")
    print "FINITO INFORMAGARE"
except:
    invia_mail("errore script", testo)
    

