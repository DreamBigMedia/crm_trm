from datetime import datetime
from mongoengine import *
import datetime
class Customer(Document):

 fname = StringField()
 lname = StringField( )
 card = StringField("Creditcard")
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
 visitor_id = IntField()

class Creditcard(BaseDocument):
 _table_ = "Creditcards"
 id = IntField(primary_key=True)
 card_number = StringField()
 ccv = StringField()
 exp_month = StringField()
 exp_year = StringField()
 IntegerField = StringField()
 billing_address2 = StringField()
 billing_city = StringField()
 billing_zipcode = IntField()
 active_card = BooleanField(default=False)
 # orders = Set("Order")

class Product(BaseDocument):
 id = IntField(primary_key=True)
 name = StringField(default="")
 salestype = StringField(choices=["straight","trial"])
 #order = IntegerField(")
 #upsell = Required(, nullable=True)
 init_price = FloatField( default=0.00)
 rebill_price = FloatField(default=0.00)

class Order(Product):
 order_number = IntField(int, unique=True)
 creditcard = ListField(Creditcard)
 products = ListField(Product)
 tracking = IntField()
 order_date = DateTimeField(datetime)
 success = BooleanField(bool)
 server_response = StringField(default="")
 email_buy = BooleanField( default=False)

class Email(BaseDocument):
 id = EmailField(primary_key=True)
 partial_id = IntField()
 optin_time = DateTimeField(datetime)
 purchased = BooleanField(default=False)
 followup = BooleanField(default=False)
 followup2 = BooleanField( default=False)
 followup3 = BooleanField(default=False)

class Visitor(BaseDocument):
 id = IntField(primary_key=True)
 c1 = StringField(str)
 c2 = StringField()
 c3 = StringField()
 c4 = StringField()
 c5 = StringField()
 trafficsource = StringField(, default="unknown")
 conversion = BooleanField(default=False)
 engage = BooleanField()
 useragent = StringField()
 referer = URLField()
 convert = BooleanField()
 lander = URLField()
