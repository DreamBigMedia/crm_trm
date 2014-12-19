from datetime import datetime
from mongoengine import *
import datetime
class Customer(Document):

 fname = StringField(unicode)
 lname = StringField(unicode, unique=True)
 card = StringField("Creditcard")
 email = EmailField(unicode)
 ship_address1 = StringField(unicode)
 ship_address2 = StringField(unicode)
 ship_city = StringField(unicode)
 ship_state = StringField(unicode)
 ship_phone = StringField(int)
 ship_zipcode = StringField(unicode)
 partial = BooleanField(default=True)
 partial_time = DateTimeField(default=datetime.datetime.now())
 order_time = DateTimeField()
 recurring = BooleanField(bool, default=False)
 visitor_id = IntField()

class Creditcard(BaseDocument):
 _table_ = "Creditcards"
 id = IntField(primary_key=True)
 card_number = StringField(unicode)
 ccv = StringField(unicode)
 exp_month = StringField(int)
 exp_year = StringField(int)
 IntegerField = StringField(unicode)
 billing_address2 = StringField(unicode)
 billing_city = StringField(unicode)
 billing_zipcode = IntField(unicode)
 active_card = BooleanField(bool)
 # orders = Set("Order")

class Product(BaseDocument):
 id = IntField(primary_key=True)
 name = StringField(default="")
 salestype = StringField(choices=["straight","trial"])
 #order = IntegerField(")
 #upsell = Required(unicode, nullable=True)
 init_price = FloatField( default=0.00)
 rebill_price = FloatField(default=0.00)

class Order(Product):
 order_number = IntField(int, unique=True)
 creditcard = ListField(Creditcard)
 products = ListField(Product)
 tracking = IntField(unicode)
 order_date = DateTimeField(datetime)
 success = BooleanField(bool)
 server_response = F(LongUnicode)
 email_buy = Required(bool, default=False)

class Email(db.Entity):
 id = EmailField(int, auto=True)
 optin_time = Required(datetime)
 purchased = Required(bool, default=False)
 followup = Required(bool, default=false)
 followup2 = Required(bool, default=false)
 followup3 = Required(bool, default=false)

class Visitor(db.Entity):
 c1 = StringField(str)
 c2 = StringField(unicode)
 c3 = StringField(unicode)
 c4 = StringField(unicode)
 c5 = StringField(unicode)
 trafficsource = StringField(unicode, default=unknown)
 conversion = BooleanField(default=True)
 engage = BooleanField(bool)
 useragent = StringField(str)
 referer = URLField(unicode)
 convert = Optional(Customer)
 id = PrimaryKey(unicode)
 lander = Required(str, lazy=False)
