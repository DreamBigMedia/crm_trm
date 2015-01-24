import datetime, models

from flask import Flask

from flask.ext import admin
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin.form import rules
from flask.ext.admin.actions import action
from flask.ext.admin.contrib.mongoengine import ModelView

app = Flask(__name__)

app.config['SECRET_KEY'] = '98fj3q9p'
app.config['MONGODB_SETTINGS'] = {'DB': 'trm'}

db = MongoEngine()
db.init_app(app)

class OrderView(ModelView):
	column_filters = ['affid', 'creditcard', 'success']
	column_searchable_list = ('affid', 'creditcard', 'products')
#	form_ajax_refs = { 'creditcard': {'fields': ('affid', 'success') } }

class CustomerView(ModelView):
	column_filters = ['fname', 'lname', 'card', 'ship_zipcode', 'order_time', 'email']
	column_searchable_list = ('fname', 'lname', 'card', 'ship_zipcode')

class NMIAccountView(ModelView):
	column_filters = ['url']
	column_searchable_list = ('prod_id', 'username', 'name')

class RebillView(ModelView):
	column_filters = ['pid', 'batched', 'affid', 'retrynum', 'nmi_id']
	column_searchable_list = ('pid', 'card', 'customer')

class AffiliateView(ModelView):
	column_searchable_list = ('username', 'affid', 'displayname')

class SmtpserverView(ModelView):
	column_filters = ['storeid', 'host', 'port', 'username', 'password', 'theme']

@app.route('/refund/')
def refund():
	return '<html><body><form method="POST" action="/do_refund/">Order<input type="text"'

@app.route('/')
def index():
	return '<html><body>lol <a href="/admin/">h4x</a></body></html>'

if __name__=='__main__':
	admin= admin.Admin(app, 'datDash')

	admin.add_view(OrderView(models.Order))
	admin.add_view(CustomerView(models.Customer))
	admin.add_view(NMIAccountView(models.NMIAccount))
	admin.add_view(RebillView(models.Rebill))
	admin.add_view(AffiliateView(models.Affiliate))
	admin.add_view(SmtpserverView(models.Smtpserver))

	app.run(debug=True, port=4200, host='0.0.0.0')
