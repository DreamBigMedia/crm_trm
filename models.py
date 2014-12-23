from datetime import datetime
from mongoengine import *
import datetime

connect('trm')

class Customer(Document):
 fname = StringField()
 lname = StringField( )
 card = IntField() # card id
 email = EmailField()
 ship_address1 = StringField()
 ship_address2 = StringField()
 ship_city = StringField()
 ship_state = StringField()
 ship_phone = StringField()
 ship_zipcode = StringField()
 partial = BooleanField(default=True)
 partial_time = DateTimeField(default=datetime.datetime.now())
 order_time = DateTimeField()
 recurring = BooleanField(default=False)
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
 active_card = BooleanField(default=False)
 # orders = Set("Order")

class Product(Document):
 name = StringField(default="")
 salestype = StringField(choices=["straight","trial"])
 #order = IntegerField(")
 #upsell = Required(, nullable=True)
 init_price = FloatField( default=0.00)
 rebill_price = FloatField(default=0.00)

class Order(Document):
 order_number = SequenceField(unique=True)
 creditcard = StringField()
 products = StringField()
 tracking = StringField()
 order_date = DateTimeField()
 success = BooleanField()
 server_response = StringField(default="")
 email_buy = BooleanField(default=False)

class Email(Document):
 optin_time = DateTimeField(datetime)
 purchased = BooleanField(default=False)
 followup = BooleanField(default=False)
 followup2 = BooleanField( default=False)
 followup3 = BooleanField(default=False)

class Visitor(Document):
 c1 = StringField()
 c2 = StringField()
 c3 = StringField()
 c4 = StringField()
 c5 = StringField()
 trafficsource = StringField(default="unknown")
 conversion = BooleanField(default=False)
 engage = BooleanField()
 useragent = StringField()
 referer = URLField()
 convert = BooleanField()
 lander = URLField()
