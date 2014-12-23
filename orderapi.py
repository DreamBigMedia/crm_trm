from flask import request, jsonify
import processing, models, json, datetime

from mainapp import app

@app.route('/track/')
def track_hit():
 c1 = request.args.get('c1')
 c2 = request.args.get('c2')
 c3 = request.args.get('c3')
 c4 = request.args.get('c4')
 c5 = request.args.get('c5')
 trafficsource = request.args.get('t1')
 l1 = request.args.get('l1')
 vid = request.args.get('uniqid')
 useragent = request.headers.get('User-Agent')
 visitor = models.Visitor(c1= c1, c2=c2,c3= c3, c4 = c4,c5=c5, trafficsource = trafficsource,
                          conversion=False,engage=False,useragent=useragent,convert=False,lander=l1,uniqid=vid)
 visitor.save()
 vi = str(visitor.id)
 return vi

@app.route('/engage/<vid>')
def engage_hit(vid):
 visitor = models.Visitor.objects.get(uniqid=vid)
 visitor.engaged=True
 visitor.save()
 vi = str(visitor.id)
 return vi

@app.route("/api/customer", methods=["POST"])
def apiCustomer():
    newguy = models.Customer(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), ship_address1=request.form.get('ship_address1'), ship_address2=request.form.get('ship_address1'), ship_city=request.form.get('ship_city'), ship_state=request.form.get('ship_state'), ship_phone=request.form.get('ship_phone'), ship_zipcode=request.form.get('ship_zipcode'))
    newguy.save()
    return str(newguy.id)

@app.route("/api/update/customer/<cid>", methods=["POST"])
def apiUpdateCustomer(cid):
    oldguy = models.Customer.orders(id=cid)
    for x in request.args['fields'].split(','):
        oldguy[x] = request.form[x]
    oldguy.save()
    return str(oldguy.id)

@app.route("/api/card", methods=["POST"])
def apiCard():
    newcard = models.Creditcard(billing_address1=request.form.get('billing_address1'), billing_address2=request.form.get('billing_address2'), billing_city=request.form.get('billing_city'), billing_state=request.form.get('billing_state'), billing_zipcode=request.form.get('billing_zipcode'), activecard=bool(request.form.get('activecard')))
    newcard.save()
    return str(newcard.id)

@app.route("/api/update/card/<cid>", methods=["POST"])
def apiUpdateCard(cid):
    oldcard = models.Creditcard.objects(id=cid)
    for x in request.args['fields'].split(','):
        oldcard[x] = request.form[x]
    oldcard.save()
    return str(oldcard.id)

@app.route("/api/orderWithCard/<customerid>")
def apiOrderWithCard(customerid):
    newcard = models.Creditcard(card_number=request.form['card_number'], ccv=request.form['ccv'], exp_month=request.form['exp_month'], exp_year=request.form['exp_year'], billing_address1=request.form['billing_address1'], billing_address2=request.form.get('billing_address2'), billing_city=request.form['billing_city'], billing_zipcode=int(request.form['billing_zipcode']))
    newcard.save()
    process = processing.uCrm({'cc_number': request.form['card_number'],
                                 'cc_month': request.form['cc_month'],
                                 'cc_year': request.form['cc_year'],
                                 'cc_cvv': request.form['ccv'],
                                 'amount': request.form['amount'],
                                 'pid': request.form['pid'],
                                 'storeid': request.form['storeid'],
                                 'fname': request.form['fname'],
                                 'lname': request.form['lname'],
                                 'address': request.form['billing_address1'],
                                 'address2': request.form['billing_address2'],
                                 'city': request.form['billing_city'],
                                 'state': request.form['billing_state'],
                                 'postal': request.form['billing_zipcode'],
                                 'billingsame': bool(request.form['billingsame']),
                                 'email': request.form['email'],
                                 'phone': request.form['billing_phone'],
                                 'cacode': request.form['cacode'],
                                 'affid': request.form['affid'],
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': request.remote_addr,
                                 'orderpage': request.form['orderpage']}).process()
    neworder = models.Order(creditcard=newcard, products=request.form['pid'], tracking=int(request.form['tracking']), order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response, recurring=bool(request.form['recurring']))
    neworder.save()
    oldguy = models.Customer.objects(id=customerid)[0]
    oldguy['card'] = newcard.id
    oldguy['order_time'] = datetime.datetime.now()
    oldguy.save()
    return jsonify({"card": str(newcard.id), "cc_response": process.raw_response, "success": process.success})

@app.route("/api/order/<customerid>/<cardid>", methods=["POST"])
def apiOrderNoCard(customerid, cardid):
    try:
        oldcard = models.Creditcard.objects(id=cardid)[0]
    except:
        return json.dumps({'error': "could not find card"})
    try:
        oldguy = models.Customer.objects(id=customerid)[0]
    except:
        return json.dumps({'error': "could not find customer"})
    process = processing.uCrm({'cc_number': oldcard['card_number'],
                                 'cc_month': oldcard['exp_month'],
                                 'cc_year': oldcard['exp_year'],
                                 'cc_cvv': oldcard['ccv'],
                                 'amount': request.form['amount'],
                                 'pid': request.form['pid'],
                                 'storeid': request.form['storeid'],
                                 'fname': oldguy['fname'],
                                 'lname': oldguy['lname'],
                                 'address': oldcard['billing_address1'],
                                 'address2': oldcard['billing_address2'],
                                 'city': oldcard['billing_city'],
                                 'state': oldcard['billing_state'],
                                 'postal': oldcard['billing_zipcode'],
                                 'billingsame': bool(request.form['billingsame']),
                                 'email': oldguy['email'],
                                 'phone': oldguy['ship_phone'],
                                 'cacode': request.form.get('cacode'),
                                 'affid': request.form.get('affid'),
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': request.remote_addr,
                                 'orderpage': request.form.get('orderpage')}).process()
    neworder = models.Order(creditcard=str(oldcard.id), products=request.form['pid'], tracking=request.form.get('tracking'), order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
    neworder.save()
    return json.dumps({'customer': str(oldguy.id), 'neworder': str(neworder.id), "cc_response": process.raw_response})
