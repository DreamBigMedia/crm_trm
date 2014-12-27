import requests

pdata = {"card_number": "4111111111111111",
         "cvv": "303",
         "exp_month": "04",
         "exp_year": "20",
         "pid": "549e1b40e998f423dd95e407",
         "quantity": 1,
         "billingsame": 'yes',
         "uniqid": "YES I AM SPECiAL"}
print requests.post("http://127.0.0.1:55555/api/orderWithCard/549e189de998f4237f1d0625/5494f153e998f4592a9704a8", pdata).text
