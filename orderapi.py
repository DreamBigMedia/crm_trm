from flask import request
import processing
import models
import json

from mainapp import app

@app.route("/api/customer", methods=["POST"])
def apiCustomer():
    newguy = models.Customer(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), ship_address1=request.form.get('ship_address1'), ship_address2=request.form.get('ship_address1'), ship_city=request.form.get('ship_city'), ship_state=request.form.get('ship_state'), ship_phone=request.form.get('ship_phone'), ship_zipcode=request.form.get('ship_zipcode'))
    newguy.save()
    return str(newguy.id)

@app.route("/api/update/customer/<int:cid>", methods=["POST"])
def apiUpdateCustomer(cid):
    oldguy = models.Customer.orders(id=cid)
    for x in request.args['fields'].split(','):
        oldguy[x] = request.form[x]
    oldguy.save()
    return oldguy

@app.route("/api/card", methods=["POST"])
def apiCard():
    newcard = models.Creditcard(billing_address1=request.form.get('billing_address1'), billing_address2=request.form.get('billing_address2'), billing_city=request.form.get('billing_city'), billing_zipcode=request.form.get('billing_zipcode'), activecard=bool(request.form.get('activecard')))
    newcard.save()
    return str(newcard.id)

@app.route("/api/update/card/<int:cid>", methods=["POST"])
def apiUpdateCard(cid):
    oldcard = models.Creditcard.objects(id=cid)
    for x in request.args['fields'].split(','):
        oldcard[x] = request.form[x]
    oldcard.save()
    return json.dumps(oldcard)

@app.route("/api/orderWithCard/<int:customerid>")
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
    return {"card": newcard.id, "cc_response": process.raw_response}

@app.route("/api/order/<int:customerid>/<int:cardid>", methods=["POST"])
def apiOrderNoCard(customerid, cardid):
    try:
        oldcard = models.Creditcard.objects(id=cardid)[0]
    except:
        return {'error': "could not find card"}
    try:
        oldguy = models.Customer.objects(id=customerid)[0]
    except:
        return {'error': "could not find customer"}
    process = processing.uCrm({'cc_number': oldcard['card_number'],
                                 'cc_month': oldcard['cc_month'],
                                 'cc_year': oldcard['cc_year'],
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
                                 'cacode': request.form['cacode'],
                                 'affid': request.form['affid'],
                                 'c1': request.form.get('c1'),
                                 'c2': request.form.get('c2'),
                                 'c3': request.form.get('c3'),
                                 'ip': request.remote_addr,
                                 'orderpage': request.form['orderpage']}).process()
    neworder = models.Order(creditcard=oldcard, products=request.form['pid'], tracking=int(request.form['tracking']), order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
    neworder.save()
    return {'customer': oldguy, 'neworder': neworder}
