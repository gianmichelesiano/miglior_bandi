import requests
from firebase import firebase
import DBconnection

conn= DBconnection.connection()
cursore = conn.cursor()

def creaMessaggio(categoria,provincie):
    conn= DBconnection.connection()
    cursore = conn.cursor()
    cursore.execute("SELECT count(*) FROM gare.GARE_NEW where DATA_SCADENZA > NOW() and ENTE <> ''") 
    gare = cursore.fetchall()
    numero_gare_totali = gare[0][0]
    testo = 'Aggiornamento sono attualmente disponibili ' + str(numero_gare_totali) +' gare'
    return testo

def inviaPush(token, messaggio):
    # il nome del profilo nel certificato dei settings di ionic
    tag = 'bandigare'
    # arriva da apikey di setting ionic
    bearer = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1MjFjYzc5Ny01M2JjLTRlZjItOTI0OC1iMGI0YTMzMDFkNTYifQ.C3jsIy1LsZacFLpEELNCVWIhhYazdhiksnq4AZgBoB8"
    url = "https://api.ionic.io/push/notifications"
                                       
    payload = "{\r\n    \"tokens\": [\""+token+"\"],\r\n    \"profile\": \""+tag+"\",\r\n    \"notification\": {\r\n        \"message\": \" "+messaggio+" \"\r\n    }\r\n}"
    headers = {
        'content-type': "application/json",
        'authorization': bearer,
        'cache-control': "no-cache",
        
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


firebase = firebase.FirebaseApplication('https://bandigare-8096d.firebaseio.com', None)
utenti = firebase.get('/utenti', None)

for key in utenti:
    try:
        impostazioni = utenti[key]
        if 'preferenze' in impostazioni:
            preferenze = utenti[key]['preferenze']
            mail = preferenze['mail']
            notifiche = preferenze['notifiche']
            if notifiche:
                # sono liste
                categoria = preferenze['categoria']
                provincie = preferenze['provincia']
                messaggio = creaMessaggio(categoria,provincie)

                if 'notifiche' in impostazioni:
                    notifiche = utenti[key]['notifiche']
                    if 'pushToken' in notifiche:
                        token = notifiche['pushToken']
                inviaPush(token, messaggio)
    except:
        pass



