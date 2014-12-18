from datetime import datetime
from peewee import *
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
    visitor_id = IntegerField()

class Creditcard(BaseDocument):
    _table_ = "Creditcards"
    id = PrimaryKeyField()
    card_number = StringField(unicode)
    ccv = StringField(unicode)
    exp_month = StringField(int)
    exp_year = StringField(int)
    IntegerField = StringField(unicode)
    billing_address2 = StringField(unicode)
    billing_city = StringField(unicode)
    billing_zipcode = IntegerField(unicode)
    active_card = BooleanField(bool)
    # orders = Set("Order")

class Product(BaseDocument):
    id = PrimaryKeyField()
    name = StringField(default="")
    salestype = StringField(choices=["straight","trial"])
    #order = IntegerField(")
    #upsell = Required(unicode, nullable=True)
    init_price = FloatField( default=0.00)
    rebill_price = FloatField(default=0.00)

class Order(db.Customer):
    order_number = Required(int, unique=True, column="Orders")
    creditcard = Required(Creditcard)
    products = Set(Product)
    tracking = Required(unicode)
    order_date = Required(datetime)
    success = Required(bool)
    server_response = Optional(LongUnicode)
    email_buy = Required(bool, default=False)

class Email(db.Entity):
    id = EmailField(int, auto=True)
    optin_time = Required(datetime)
    purchased = Required(bool, default=False)
    followup = Required(bool, default=false)
    followup2 = Required(bool, default=false)
    followup3 = Required(bool, default=false)

class Visitor(db.Entity):
    c1 = Optional(str)
    c2 = Required(unicode)
    c3 = Required(unicode)
    c4 = Required(unicode)
    c5 = Required(unicode)
    trafficsource = Optional(unicode, default=unknown)
    conversion = Required(bool)
    engage = Required(bool)
    useragent = Required(str)
    referer = Optional(unicode)
    convert = Optional(Customer)
    id = PrimaryKey(unicode)
    lander = Required(str, lazy=False)
