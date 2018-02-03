if 1:
        testo = "ANAC"
        execfile("ANAC//AVCP_cerca.py")
        print "FINITO CERCA ANAC"
        execfile("ANAC//insert_db.py")
        print "FINITO INSERT ANAC"
        testo = "SCP"
        print "inizioSTP"
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
        print "FINITO FIREBASE"
        invia_mail("FINITO", "finito")
        print "MAIL INVIATA"
