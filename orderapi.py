from flask import request, jsonify, Flask
import processing, models, json, datetime

app = Flask(__name__)

@app.route('/track/')
def track():
 c1 = request.args.get('c1')
 c2 = request.args.get('c2')
 c3 = request.args.get('c3')
 c4 = request.args.get('c4')
 c5 = request.args.get('c5')
 trafficsource = request.args.get('t1')
 l1 = request.args.get('l1')
 vid = request.args.get('uniqid')
 useragent = request.headers.get('User-Agent')
 visitor = models.Visitor(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, trafficsource=trafficsource, conversion=False, engage=False, useragent=useragent, convert=False, lander=l1, uniqid=vid)
 visitor.save()
 vi = str(visitor.id)
 return vi

@app.route('/engage/<vid>')
def engage_hit(vid):
 visitor = models.Visitor.objects.get(id=vid)
 visitor.engage=True
 visitor.save()
 vi = str(visitor.id)
 return vi

@app.route("/api/get/customer/<cid>")
def apiGetCustomer(cid):
    oldguy = models.Customer().objects({'id': cid})
    return oldguy[0]

@app.route("/api/customer", methods=["POST"])
def apiCustomer():
    newguy = models.Customer(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), ship_address1=request.form.get('ship_address1'), ship_address2=request.form.get('ship_address2'), ship_city=request.form.get('ship_city'), ship_state=request.form.get('ship_state'), ship_phone=request.form.get('ship_phone'), ship_zipcode=request.form.get('ship_zipcode'))
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

@app.route("/api/orderWithCard/<processor>/<customerid>", methods=["POST"])
def apiOrderWithCard(processor, customerid):
    try:
        oldguy = models.Customer.objects(id=customerid)[0]
    except:
        return jsonify({"success": False, "cc_response": "invalid customer"})
    if request.form['billingsame'].lower().startswith('y'):
        billingsame = True
    else:
        billingsame = False
    remoteaddr = request.remote_addr
    if 'X-Forwarded-For' in request.headers.keys():
        remoteaddr = request.headers['X-Forwarded-For'].strip()
    if ', ' in remoteaddr:
        remoteaddr = remoteaddr.split(', ')[1]
    try:
        bill_zip = int(request.form['billing_zipcode'])
    except:
        bill_zip = 0
    newcard = models.Creditcard(card_number=request.form['card_number'], ccv=request.form['cvv'], exp_month=request.form['exp_month'], exp_year=request.form['exp_year'], billing_address1=request.form.get('billing_address1'), billing_address2=request.form.get('billing_address2'), billing_city=request.form.get('billing_city'), billing_zipcode=bill_zip)
    if billingsame:
        newcard.billing_address1 = oldguy['ship_address1']
        newcard.billing_address2 = oldguy['ship_address2']
        newcard.billing_city = oldguy['ship_city']
        newcard.billing_state = oldguy['ship_state']
        newcard.billing_zipcode = oldguy['ship_zipcode']
        newcard.billing_country = 'us'
    newcard.save()
    if processor == "ucrm":
        process = processing.uCrm({'cc_number': request.form['card_number'],
                                 'cc_month': request.form['exp_month'],
                                 'cc_year': request.form['exp_year'],
                                 'cc_cvv': request.form['cvv'],
                                 'amount': request.form['amount'],
                                 'pid': request.form['pid'],
                                 'storeid': request.form['storeid'],
                                 'fname': oldguy['fname'],
                                 'lname': oldguy['lname'],
                                 'address': oldguy['ship_address1'],
                                 'address2': oldguy['ship_address2'],
                                 'city': oldguy['ship_city'],
                                 'state': oldguy['ship_state'],
                                 'postal': oldguy['ship_zipcode'],
                                 'billing_fname': request.form.get('fname'),
                                 'billing_lname': request.form.get('lname'),
                                 'billing_address': request.form.get('billing_address1'),
                                 'billing_address2': request.form.get('billing_address2'),
                                 'billing_city': request.form.get('billing_city'),
                                 'billing_state': request.form.get('billing_state'),
                                 'billing_postal': request.form.get('billing_zipcode'),
                                 'billingsame': billingsame,
                                 'email': oldguy['email'],
                                 'phone': oldguy['ship_phone'],
                                 'cacode': request.form['cacode'],
                                 'affid': request.form['affid'],
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': remoteaddr,
                                 'orderpage': request.form['orderpage']}).process()
    elif processor == "stripe":
        try:
            prod = models.Product.objects({'id': request.form['pid']})[0]
        except:
            return jsonify({"success": False, "cc_response": "invalid product id"})
        if int(request.form['quantity']) > 1:
            prodname = prod['name'] + " x"+request.form['quantity']
            prodamount = int(prod['amount']*100*int(request.form['quantity']))
        else:
            prodname = prod['name']
            prodamount = int(prod['amount']*100)
        process = processing.Stripe({'cc_number': request.form['card_number'],
                                 'cc_month': request.form['exp_month'],
                                 'cc_year': request.form['exp_year'],
                                 'cc_cvv': request.form['cvv'],
                                 'amount': prod['amount']*int(request.form['quantity']),
                                 'product': prodname,
                                 'pid': request.form['pid'],
                                 'fname': request.form['fname'],
                                 'lname': request.form['lname'],
                                 'address': request.form['ship_address1'],
                                 'address2': request.form['ship_address2'],
                                 'city': request.form['ship_city'],
                                 'state': request.form['ship_state'],
                                 'postal': request.form['ship_zipcode'],
                                 'billingsame': True,
                                 'email': request.form['email'],
                                 'phone': request.form['ship_phone'],
                                 'cacode': request.form['cacode'],
                                 'affid': request.form['affid'],
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': remoteaddr,
                                 'orderpage': request.form['orderpage']}).process()
    else:
        return jsonify({"success": False, "cc_response": "invalid processor"})
    neworder = models.Order(creditcard=str(newcard.id), products=request.form['pid'], tracking=request.form['uniqid'], order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
    neworder.save()
    oldguy['card'] = str(newcard.id)
    oldguy['order_time'] = datetime.datetime.now()
    oldguy.save()
    return jsonify({"card": str(newcard.id), "cc_response": process.raw_response, "success": process.success, "order": str(neworder.id)})

@app.route("/api/order/<processor>/<customerid>/<cardid>", methods=["POST"])
def apiOrderNoCard(processor, customerid, cardid):
    try:
        oldcard = models.Creditcard.objects(id=cardid)[0]
    except:
        return jsonify({'cc_response': "could not find card", "success": False})
    try:
        oldguy = models.Customer.objects(id=customerid)[0]
    except:
        return jsonify({'cc_response': "could not find customer", "success": False})
    remoteaddr = request.remote_addr
    if 'X-Forwarded-For' in request.headers.keys():
        remoteaddr = request.headers['X-Forwarded-For']
    if ', ' in remoteaddr:
        remoteaddr = remoteaddr.split(', ')[1]
    if processor == "ucrm":
        process = processing.uCrm({'cc_number': oldcard['card_number'],
                                 'cc_month': oldcard['exp_month'],
                                 'cc_year': oldcard['exp_year'],
                                 'cc_cvv': oldcard['ccv'],
                                 'amount': request.form['amount'],
                                 'pid': request.form['pid'],
                                 'storeid': request.form['storeid'],
                                 'fname': oldguy['fname'],
                                 'lname': oldguy['lname'],
                                 'address': oldguy['ship_address1'],
                                 'address2': oldguy['ship_address2'],
                                 'city': oldguy['ship_city'],
                                 'state': oldguy['ship_state'],
                                 'postal': oldguy['ship_zipcode'],
                                 'billing_fname': oldguy['fname'],
                                 'billing_lname': oldguy['lname'],
                                 'billing_address': oldcard['billing_address1'],
                                 'billing_address2': oldcard['billing_address2'],
                                 'billing_city': oldcard['billing_city'],
                                 'billing_state': oldcard['billing_state'],
                                 'billing_postal': oldcard['billing_zipcode'],
                                 'billingsame': False,
                                 'email': oldguy['email'],
                                 'phone': oldguy['ship_phone'],
                                 'cacode': request.form['cacode'],
                                 'affid': request.form['affid'],
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': remoteaddr,
                                 'orderpage': request.form['orderpage']}).process()
    elif processor == "stripe":
        try:
            prod = models.Product.objects({'id': request.form['pid']})[0]
        except:
            return jsonify({"success": False, "cc_response": "invalid product id"})
        if int(request.form['quantity']) > 1:
            prodname = prod['name'] + " x"+request.form['quantity']
        else:
            prodname = prod['name']
        if int(request.form['quantity']) > 1:
            prodname = prod['name'] + " x"+request.form['quantity']
            prodamount = int(prod['amount']*100*int(request.form['quantity']))
        else:
            prodname = prod['name']
            prodamount = int(prod['amount']*100)
        process = processing.Stripe({'cc_number': oldcard['card_number'],
                                 'cc_month': oldcard['cc_month'],
                                 'cc_year': oldcard['cc_year'],
                                 'cc_cvv': oldcard['ccv'],
                                 'amount': prod['amount']*int(request.form['quantity']),
                                 'product': prodname,
                                 'pid': request.form['pid'],
                                 'storeid': request.form['storeid'],
                                 'fname': oldguy['fname'],
                                 'lname': oldguy['lname'],
                                 'address': oldcard['billing_address1'],
                                 'address2': oldcard['billing_address2'],
                                 'city': oldcard['billing_city'],
                                 'state': oldcard['billing_state'],
                                 'postal': oldcard['billing_zipcode'],
                                 'billingsame': True,
                                 'email': oldguy['email'],
                                 'phone': oldguy['ship_phone'],
                                 'cacode': request.form['cacode'],
                                 'affid': request.form['affid'],
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': remoteaddr,
                                 'orderpage': request.form['orderpage']}).process()
    else:
        return jsonify({"success": False, "cc_response": "invalid processor"})
    neworder = models.Order(creditcard=str(oldcard.id), products=request.form['pid'], tracking=request.form['uniqid'], order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
    neworder.save()
    return jsonify({"card": str(oldcard.id), "cc_response": process.raw_response, "success": process.success, "order": str(neworder.id)})

if __name__=="__main__":
  app.run(host="0.0.0.0", port=55555, debug=True)
