import json
import DBconnection
conn= DBconnection.connection()



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
    d = json.load(json_data)

def trova_geo(cap_da_trovare):
    for uno in d:
        if cap_da_trovare in uno['cap']:
            print  uno['nome']
            print uno['codice']
            sql = "SELECT Comune,PROVINCIA, REGIONE FROM gare.comuni_abitanti where Istat  = "+ str(uno['codice'])
            print sql
            cursore = conn.cursor()
            cursore.execute(sql)
            valori  =  cursore.fetchone()
        else:
            cap_da_trovare = cap_da_trovare[:3]+"xx"
            sql = "SELECT Comune,PROVINCIA, REGIONE FROM gare.comuni_abitanti where CAP  = '"+ str(cap_da_trovare)+"'"
            print sql
            cursore = conn.cursor()
            cursore.execute(sql)
            valori  =  cursore.fetchone()
        citta = valori[0]
        prov  = valori[1]
        regione = dict_reg[valori[2]]
        return (citta, prov, regione)
        
        

        
cap_vare = '50100'
print trova_geo(cap_vare)


