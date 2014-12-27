import requests

pdata = {"card_number": "4111111111111111",
         "cvv": "303",
         "exp_month": "04",
         "exp_year": "20",
         "pid": "549a83c609d0245cdb951618",
         "quantity": 1,
         "billingsame": 'yes',
         "uniqid": "YES I AM SPECiAL"}
print requests.post("http://162.218.236.81:55555/api/orderWithCard/549e245309d02402762df3a9/5494f153e998f4592a9704a8", pdata).text
