import models, datetime
from flask import request, render_template

from mainapp import app

@app.route("/backside")
def backside():
    return render_template('index.html')

@app.route("/backside/visitors")
def backsideHits():
    skip = request.args.get('start')
    limit = request.args.get('num')
    if skip=='':
        skip = 0
    else:
        skip = int(skip)
    if limit == '':
        limit = 100
    else:
        limit = int(limit)
    visitors = {}
    for x in models.Visitor.objects().skip(skip).limit(limit):
        visitors[str(x.id)] = {'c1': x.c1, 'c2': x.c2, 'c3': x.c3, 'c4': x.c4, 'c5': x.c5,
                          'trafficsource': x.trafficsource, 'conversion': x.conversion, 'engage': x.engage,
                          'useragent': x.useragent, 'referer': x.referer, 'convert': x.convert, 'lander': x.lander}
    return visitors

@app.route("/backside/emails")
def backsideEmail():
    if request.method == "GET":
        skip = request.args.get('start')
        limit = request.args.get('num')
        if skip=='':
            skip = 0
        else:
            skip = int(skip)
        if limit == '':
            limit = 100
        else:
            limit = int(limit)
        emails = {}
        for x in models.Email.objects().skip(skip).limit(limit):
            emails[str(x.id)] = {'optin_time': x.optin_time, 'purchased': x.purchased, 'followup': x.followup, 'followup2': x.followup2, 'followup3': x.followup3}
        return emails
    else:
        return "ERROR: unsupported http method"

@app.route("/backside/orders")
def backsideOrders():
    if request.method == "GET":
        skip = request.args.get('start')
        limit = request.args.get('num')
        if skip=='':
            skip = 0
        else:
            skip = int(skip)
        if limit == '':
            limit = 100
        else:
            limit = int(limit)
        orders = {}
        for x in models.Order.objects().skip(skip).limit(limit):
            orders[str(x.id)] = {'order_number': x.order_number, 'creditcard': x.creditcard, 'products': x.products, 'tracking': x.tracking, 'order_date': x.order_date, 'success': x.success, 'server_response': x.server_response, 'email_buy': x.email_buy}
        return orders
    else:
        return "ERROR: unsupported http method"

@app.route("/backside/filter/orders/<fields>")
def backsideFilterOrders(fields):
    fields = fields.split(",")
    kwdict = {}
    for x in fields:
        kwdict[x] = request.args[x]
    skip = request.args.get('start')
    limit = request.args.get('num')
    if skip == '':
        skip = 0
    else:
        skip = int(skip)
    if limit == '':
        limit = 100
    else:
        limit = int(limit)
    orders = {}
    for x in models.Order.objects(**kwdict).skip(skip).limit(limit):
        order[str(x.id)] = {'order_number': x.order_number, 'creditcard': x.creditcard, 'products': x.products, 'tracking': x.tracking, 'order_date': x.order_date, 'success': x.success, 'server_response': x.server_response, 'email_buy': x.email_buy}
    return orders

@app.route("/backside/products", methods=["GET", "POST"])
def backsideProduct():
    if request.method == "GET":
        skip = request.args.get('start')
        limit = request.args.get('num')
        if skip=='':
            skip = 0
        else:
            skip = int(skip)
        if limit == '':
            limit = 100
        else:
            limit = int(limit)
        products = {}
        for x in models.Product.objects():
            products[str(x.id)] = {'name': x.name, 'salestype': x.salestype, 'init_price': x.init_price, 'rebill_price': x.rebill_price}
        return products
    elif request.method == "POST":
        newproduct = models.Product(name=request.form['name'], salestype=request.form['salestype'], init_price=float(request.form['init_price']), rebill_price=float(request.form['rebill_price']))
        newproduct.save()
        return str(newproduct.id)
    else:
        return "ERROR: unsupported http method"

@app.route("/backside/filter/products/<fields>")
def backsideFilterProducts(fields):
    fields = fields.split(',')
    kwdict = {}
    for x in fields:
        kwdict[x] = request.args[x]
    skip = request.args.get('start')
    limit = request.args.get('num')
    if skip == '':
        skip = 0
    else:
        skip = int(skip)
    if limit == '':
        limit = 100
    else:
        limit = int(limit)
    products = {}
    for x in models.Product.objects(**kwdict).skip(skip).limit(limit):
        products[str(x.id)] = {'name': x.name, 'salestype': x.salestype, 'init_price': x.init_price, 'rebill_price': x.rebill_price}
    return products

@app.route("/backside/creditcards", methods=["GET", "POST"])
def backsideCreditcards():
    if request.method == "GET":
        skip = request.args.get('start')
        limit = request.args.get('num')
        if skip=='':
            skip= 0
        else:
            skip = int(skip)
        if limit == '':
            limit = 100
        else:
            limit = int(limit)
        creditcards = {}
        for x in models.Creditcard.objects().skip(skip).limit(limit):
            creditcards[str(id)] = {'card_number': x.card_number, 'ccv': x.ccv, 'exp_month': x.exp_month, 'exp_year': x.exp_year, 'billing_address': x.billing_address, 'billing_city': x.billing_city, 'billing_zipcode': x.billing_zipcode, 'active_card': x.active_card}
        return creditcards
    elif request.method == "POST":
        newcard = models.Creditcard(card_number=request.form['card_number'], ccv=request.form['ccv'], exp_month=request.form['exp_month'], exp_year=request.form['exp_year'], billing_address=request.form['billing_address'], billing_address2=request.form['billing_address2'], billing_city=request.form['billing_city'], billing_zipcode=int(request.form['billing_zipcode']), active_card=bool(request.form['active_card']))
        newcard.save()
        return str(newcard.id)
    else:
        return "ERROR: unsupported http method"

@app.route("/backside/customers", methods=["GET", "POST"])
def backsideCustomers():
    if request.method == "GET":
        skip = request.args.get('start')
        limit = request.args.get('num')
        if skip=='':
            skip= 0
        else:
            skip = int(skip)
        if limit == '':
            limit = 100
        else:
            limit = int(limit)
        customers = {}
        for x in models.Customer.objects().skip(skip).limit(limit):
            customers[str(x.id)] = {'fname': x.fname, 'lname': x.lname, 'card': x.card, 'email': x.email, 'ship_address1': x.ship_address1, 'ship_address2': x.ship_address2, 'ship_city': x.ship_city, 'ship_phone': x.ship_phone, 'ship_zipcode': x.ship_zipcode, 'partial': x.partial, 'partial_time': x.partial_time, 'order_time': x.order_time, 'recurring': x.recurring, 'visitor_id': x.visitor_id}
        return customers
    elif request.method == "POST":
        newcustomer = models.Customer(fname=request.form['fname'], lname=request.form['lname'], card=request.form['card'], email=request.form['email'], ship_address1=request.form['ship_address1'], ship_address2=request.form['ship_address2'], ship_city=request.form['ship_city'], ship_state=request.form['ship_state'], ship_phone=request.form['ship_phone'], ship_zipcode=request.form['ship_zipcode'], partial=bool(request.form['partial']), order_time=datetime.datetime.now(), recurring=bool(request.form['recurring']))
        newcustomer.save()
        return str(newcustomer.id)
    else:
        return "ERROR: unsupported http method"

@app.route("/backside/filter/customers/<fields>")
def backsideFilterCustomers(fields):
    fields = fields.split(',')
    kwdict = {}
    for x in fields:
        kwdict[x] = request.args[x]
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    if skip == '':
        skip = 0
    else:
        skip = int(skip)
    if limit == '':
        limit = 100
    else:
        limit = int(limit)
    customers = {}
    for x in models.Customer.objects(**kwdict).skip(skip).limit(limit):
        customers[str(x.id)] = {'fname': x.fname, 'lname': x.lname, 'card': x.card, 'email': x.email, 'ship_address1': x.ship_address1, 'ship_address2': x.ship_address2, 'ship_city': x.ship_city, 'ship_state': x.ship_state, 'ship_phone': x.ship_phone, 'ship_zipcode': x.ship_zipcode, 'partial': x.partial, 'partial_time': x.partial_time, 'order_time': x.order_time, 'recurring': x.recurring, 'visitor_id': x.visitor_id}
    return customers
