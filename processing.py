import requests, datetime, stripe, json
from minFraud import minFraud
from settings import SETTINGS

stripe.api_key = SETTINGS['stripe']['apikey']

class cashResponse:
 success = False
 errorMessage = ""
 raw_response = {}
 str_response = ""
 orderid = ""
 amount = 0
 mytype = ''
 def __init__(self, issuccess, ordernum, errormsg, raw_resp, str_resp, billedamount, mytype='unknown'):
  self.success = issuccess
  self.errorMessage = errormsg
  self.raw_response = raw_resp
  self.str_response = str_resp
  self.amount = billedamount
  self.orderid = ordernum
  self.mytype = mytype
 def __str__(self):
  return "cashResponse("+repr(self.success)+", "+repr(self.orderid)+", "+repr(self.errorMessage)+", "+repr(self.raw_response)+", "+repr(self.str_response)+", "+repr(self.amount)+", "+repr(self.mytype)+")"

class Processor:
 realname="Generic Processor"
 codename="genericprocessor"
 card = {}
 required_fields = ['cc_number', 'cc_month', 'cc_year', 'cc_cvv', 'amount']
 optional_fields = {'email': '', 'fname': '', 'lname': '', 'postal': '', 'product': '', 'billingsame': True, 'ip': '256.256.256.256',}
 address_fields = {'fname': 'billing_fname',
                   'lname': 'billing_lname',
                   'address': 'billing_address',
                   'address2': 'billing_address2',
                   'city': 'billing_city',
                   'state': 'billing_state',
                   'postal': 'billing_postal',
                   'country': 'billing_country'}
 def __init__(self, creditcard):
  self.card = creditcard
  print repr(self.card)
 def _defaults(self):
  for x in self.optional_fields.keys():
   if x not in self.card.keys():
    self.card[x] = self.optional_fields[x]
 def _samebilling(self):
  for x in self.address_fields.keys():
   self.card[self.address_fields[x]] = self.card[x]
 def process(self):
  self._defaults()
  if self.card['billingsame']:
   self._samebilling()
  for x in self.required_fields:
   if x not in self.card.keys():
    raise ValueError('Missing required "'+x+'" field')

class Stripe(Processor):
 realname = "Stripe"
 codename = "stripe"
 required_fields = ['address', 'city', 'state', 'postal', 'cc_number', 'cc_month', 'cc_year', 'cc_cvv', 'amount']
 optional_fields = {'email': '', 'fname': '', 'lname': '', 'postal': '', 'product': '', 'billingsame':False, 'ip': '256.256.256.256'}
 def process(self):
   Processor.process(self)
   retval = stripe.Charge.create(
       amount=self.card['amount'],
       currency="usd",
       card={
         "address_city": self.card['city'],
         "address_country": "us",
         "address_line1": self.card['address'],
         "address_state": self.card['state'],
         "address_zip": self.card['postal'],
         "number": self.card['cc_number'],
         "exp_month": self.card['cc_month'],
         "exp_year": self.card['cc_year'],
         "cvc": self.card['cc_cvv']
       },
       description=self.card['product']
     )
   return cashResponse(True, retval['id'], "Success", retval, json.dumps(retval), retval['amount'], self.codename)

class uCrm(Processor):
 realname = "uCrm"
 codename = "dennis"
 required_fields = ['pid', 'fname', 'lname', 'address', 'city', 'state', 'postal', 'billingsame',
                    'cc_number', 'cc_month', 'cc_year', 'cc_cvv', 'email', 'phone', 'storeid']
 optional_fields = {'address2': '', 'country': 'us', 'cacode': 'default', 'affid': '',
                    'c1': '', 'c2': '', 'c3': '', 'test': '0', 'leadtype': '', 'ip': '256.256.256.256',
                    'orderpage': '', 'amount': '?'}
 def process(self):
  Processor.process(self)
  token = SETTINGS['ucrm']['tokens'][self.card['storeid']]
  print token
  pdata = {'type': 'sale',
         'token': token,
         'storeid': self.card['storeid'],
         'clientip': self.card['ip'],
         'saleorigin': self.card['orderpage'],
         'pid': self.card['pid'],
         'offer': self.card['cacode'],
         'caCode': self.card['cacode'],
         'affcode': self.card['affid'],
         'sfirstname': self.card['fname'],
         'slastname': self.card['lname'],
         'saddress1': self.card['address'],
         'saddress2': self.card['address2'],
         'scity': self.card['city'],
         'sstate': self.card['state'],
         'szipcode': self.card['postal'],
         'scountry': 'US',
         'bfirstname': self.card['billing_fname'],
         'blastname': self.card['billing_lname'],
         'baddress1': self.card['billing_address'],
         'baddress2': self.card['billing_address2'],
         'bcity': self.card['billing_city'],
         'bstate': self.card['billing_state'],
         'bzipcode': self.card['billing_postal'],
         'bcountry': 'US',
         'cardnumber': self.card['cc_number'],
         'expirymonth': self.card['cc_month'],
         'expiryyear': self.card['cc_year'],
         'cardcvv': self.card['cc_cvv'],
         'email': self.card['email'],
         'phonenumber': self.card['phone'],
         'leadtype': self.card['leadtype'],
         'misc1': self.card['c1'],
         'misc2': self.card['c2'],
         'misc3': self.card['c3']}
  print repr(pdata)
  retval = requests.post('https://secure1.m57media.com/gateway/', pdata, timeout=300000).text
  print retval
  retvaljson = {}
  for x in retval.split('&'):
   if '=' not in x:
    continue
   k,v = x.split('=', 1)
   retvaljson[k] = v
  return cashResponse(retvaljson['success']=='Yes', retvaljson['orderID'], retvaljson['message'], retvaljson, retval, self.card['amount'], self.codename)

class NMI(Processor):
  realname = "NMI"
  codename = "nmi"
  required_fields = ['fname', 'lname', 'address', 'city', 'state', 'postal', 'cc_number', 'cc_exp', 'cc_cvv', 'amount', 'ip', 'email']
  optional_fields = {'product': '', 'billingsame':False, 'country': 'US'}
  def __init__(self, creditcard, username, password, gateway="https://secure.networkmerchants.com/api/transact.php"):
    Processor.__init__(self, creditcard)
    self.gateway = gateway
    self.username = username
    self.password = password
  def process(self):
    self._defaults()
    pdata = {'type': 'sale',
             'username': self.username,
             'password': self.password,
             'ccnumber': self.card['cc_number'],
             'ccexp': self.card['cc_exp'],
             'amount': self.card['amount'],
             'cvv': self.card['cc_cvv'],
             'firstname': self.card['fname'],
             'lastname': self.card['lname'],
             'address1': self.card['address'],
             'city': self.card['city'],
             'state': self.card['state'],
             'zip': self.card['postal'],
             'country': self.card['country'],
             'email': self.card['email'],
             'ipaddress': self.card['ip']}
    retval = requests.post(self.gateway, pdata).text
    retvaljson = {}
    for x in retval.split('&'):
     if '=' not in x:
      continue
     k,v = x.split('=', 1)
     retvaljson[k] = v
    return cashResponse(retvaljson['response_code']=='100', retvaljson['orderid'], retvaljson['responsetext'], retvaljson, retval, self.card['amount'], self.codename)

if __name__=="__main__": #if we arent an import, run some tests
  #print ">> Stripe()"
  #ostripe = Stripe({'address': '123 fake st',
  #   'city': 'Springfield',
  #   'state': 'OH',
  #   'postal': '45501',
  #   'cc_number': '4111111111111111',
  #   'cc_month': '04',
  #   'cc_year': '2020',
  #   'cc_cvv': '303',
  #   'amount': '1000'} # $10.00
  #   )
  #print ">> Stripe.process()"
  #print str(ostripe.process())
  #print ">> uCrm()"
  #odennis = uCrm({'fname': 'Fat',
  #   'lname': 'Tony',
  #   'address': '123 fake st',
  #   'city': 'Springfield',
  #   'state': 'OH',
  #   'postal': '45501',
  #   'billingsame': True,
  #   'cc_number': '4111111111111111',
  #   'cc_month': '04',
  #   'cc_year': '2020',
  #   'cc_cvv': '303',
  #   'amount': '10.00',
  #   'email': 'datDruggie@yopmail.com',
  #   'phone': '8009001000',
  #   'storeid': '458',
  #   'pid': '12342',
  #   'test': '1'})
  #print ">> uCrm.process()"
  #print str(odennis.process())
  print ">> NMI()"
  omni = NMI({'fname': 'Fat',
     'lname': 'Tony',
     'address': '123 fake st',
     'city': 'Springfield',
     'state': 'OH',
     'postal': '45501',
     'cc_number': '4111111111111111',
     'cc_exp': '0420',
     'cc_cvv': '303',
     'amount': '10.00',
     'email': 'datDruggie@yopmail.com',
     'ip': '127.0.0.1'}, 'demo', 'password')
  print ">> NMI.process()"
  print str(omni.process())
