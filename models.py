from datetime import datetime
from mongoengine import *
import datetime

connect('trm')

class Customer(Document):
 fname = StringField()
 lname = StringField( )
 card = StringField() # card id
 email = EmailField()
 ship_address1 = StringField()
 ship_address2 = StringField()
 ship_city = StringField()
 ship_state = StringField()
 ship_phone = StringField()
 ship_zipcode = StringField()
 partial = StringField()
 partial_time = DateTimeField(default=datetime.datetime.now())
 order_time = DateTimeField()
 recurring = StringField()
 visitor_id = StringField()

class Creditcard(Document):
 _table_ = "Creditcards"
 card_number = StringField()
 ccv = StringField()
 exp_month = StringField()
 exp_year = StringField()
 billing_address1 = StringField()
 billing_address2 = StringField()
 billing_city = StringField()
 billing_state = StringField()
 billing_zipcode = IntField()
 active_card = StringField()
 # orders = Set("Order")

class Product(Document):
 name = StringField(default="")
 salestype = StringField(choices=["straight","trial"])
 rebilldays = IntField(default=0)
 init_price = FloatField(default=0.00)
 rebill_price = FloatField(default=0.00)

class Order(Document):
 order_number = SequenceField(unique=True)
 creditcard = StringField()
 products = StringField()
 tracking = StringField()
 order_date = DateTimeField()
 success = StringField()
 server_response = StringField(default="")
 email_buy = StringField()

class Email(Document):
 optin_time = DateTimeField(datetime)
 purchased = StringField()
 followup = StringField()
 followup2 = StringField()
 followup3 = StringField()

class Visitor(Document):
 c1 = StringField()
 c2 = StringField()
 c3 = StringField()
 c4 = StringField()
 c5 = StringField()
 trafficsource = StringField(default="unknown")
 conversion = StringField()
 engage = StringField()
 useragent = StringField()
 referer = URLField()
 convert = StringField()
 lander = URLField()

class NMIAccount(Document):
 name = StringField()
 url = StringField()
 username = StringField()
 password = StringField()
 batchmax = IntField(default=0)

Nmiaccount = NMIAccount # for rest api

class Rebill(Document):
 card = StringField()
 customer = StringField()
 pid = StringField()
 date = StringField()
 batched = StringField(default=False)
