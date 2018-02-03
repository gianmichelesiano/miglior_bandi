import requests
import json
serviceurl = "http://app.appalti-app.it/service/service.php"



index = 10
payload = { 'tipo':'elenco_gare_attive', 'idutente' : '' , 'from':0 }
payload['from'] = index
print serviceurl
print payload
r = requests.post(serviceurl, data=payload)
    
responce_json = json.loads(r.text)
print responce_json
