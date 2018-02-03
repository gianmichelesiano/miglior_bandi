import requests
serviceurl = 'http://www.informagare.it/risultato.php?regione=campania'


s = requests.Session()

s.post(serviceurl)
#logged in! cookies saved for future requests.

serviceurl_prov =  "http://www.informagare.it/risultato.php?provincia=BN"
r2 = s.get(serviceurl_prov)
print r2.text
