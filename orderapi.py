from flask import request, jsonify, Flask
from tMail import tMail
from nmi_utils import nmiSelect
from createsend import Subscriber
import processing, models, json, datetime, os.path

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
 remoteaddr = request.remote_addr
 if 'X-Forwarded-For' in request.headers.keys():
  remoteaddr = request.headers['X-Forwarded-For'].strip()
 if ', ' in remoteaddr:
  remoteaddr = remoteaddr.split(', ')[1]
 visitor = models.Visitor(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, trafficsource=trafficsource, conversion=False, engage=False, lead=False, useragent=useragent, convert='', lander=l1, uniqid=vid, referer=request.headers.get('Referer'), remoteaddr=remoteaddr)
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
    oldguy = models.Customer().objects(id=cid)
    return oldguy[0]

@app.route("/api/customer", methods=["POST"])
def apiCustomer():
    newguy = models.Customer(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), ship_address1=request.form.get('ship_address1'), ship_address2=request.form.get('ship_address2'), ship_city=request.form.get('ship_city'), ship_state=request.form.get('ship_state'), ship_phone=request.form.get('ship_phone'), ship_zipcode=request.form.get('ship_zipcode'))
    newguy.save()
    remoteaddr = request.remote_addr
    if 'X-Forwarded-For' in request.headers.keys():
        remoteaddr = request.headers['X-Forwarded-For'].strip()
    if ', ' in remoteaddr:
        remoteaddr = remoteaddr.split(', ')[1]
    try:
        oldvisitor = models.Visitor.objects(uniqid=request.form.get('uniqid'), remoteaddr=remoteaddr, lead=False)[0]
        oldvisitor['lead'] = True
        oldvisitor.save()
    except:
        print "couldnt find lead!"
    return str(newguy.id)

@app.route("/api/update/customer/<cid>", methods=["POST"])
def apiUpdateCustomer(cid):
    oldguy = models.Customer.objects(id=cid)
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
    oldcard = models.Creditcard.objects(id=cid)[0]
    for x in request.args['fields'].split(','):
        oldcard[x] = request.form[x]
    oldcard.save()
    return str(oldcard.id)

@app.route("/api/listme/<listid>/<cid>")
def apiListMe(listid, cid):
    oldguy = models.Customer.objects(id=cid)[0]
    return str(Subscriber({'api_key':"faf2f9d82420bc0db8c91fbf08099d8e"}).add(listid, oldguy['email'], oldguy['fname'], [], False))

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
    print str(billingsame)
    remoteaddr = request.remote_addr
    if 'X-Forwarded-For' in request.headers.keys():
        remoteaddr = request.headers['X-Forwarded-For'].strip()
    if ', ' in remoteaddr:
        remoteaddr = remoteaddr.split(', ')[1]
    try:
        bill_zip = int(request.form['billing_zipcode'])
    except:
        bill_zip = 0
    print str(bill_zip)
    newcard = models.Creditcard(card_number=request.form['card_number'], ccv=request.form['cvv'], exp_month=request.form['exp_month'], exp_year=request.form['exp_year'], billing_address1=request.form.get('billing_address1'), billing_address2=request.form.get('billing_address2'), billing_city=request.form.get('billing_city'), billing_state=request.form.get('billing_state'), billing_zipcode=bill_zip)
    if billingsame:
        newcard.billing_address1 = oldguy['ship_address1']
        newcard.billing_address2 = oldguy['ship_address2']
        newcard.billing_city = oldguy['ship_city']
        newcard.billing_state = oldguy['ship_state']
        newcard.billing_zipcode = oldguy['ship_zipcode']
        newcard.billing_country = 'us'
    newcard.save()
    print str(newcard.id)
    if processor == "ucrm":
        if billingsame:
          bsame = 'yes'
        else:
          bsame = 'no'
        process = processing.uCrm({'cc_number': newcard['card_number'],
                                 'cc_month': newcard['exp_month'],
                                 'cc_year': newcard['exp_year'],
                                 'cc_cvv': newcard['ccv'],
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
                                 'billing_address': newcard['billing_address1'],
                                 'billing_address2': request.form.get('billing_address2'),
                                 'billing_city': newcard['billing_city'],
                                 'billing_state': newcard['billing_state'],
                                 'billing_postal': newcard['billing_zipcode'],
                                 'billingsame': bsame,
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
            prod = models.Product.objects(id= request.form['pid'])[0]
        except:
            return jsonify({"success": False, "cc_response": "invalid product id"})
        if int(request.form['quantity']) > 1:
            prodname = prod['name'] + " x"+request.form['quantity']
            prodamount = int(prod['init_price']*100*int(request.form['quantity']))
        else:
            prodname = prod['name']
            prodamount = int(prod['init_price']*100)
        process = processing.Stripe({'cc_number': request.form['card_number'],
                                 'cc_month': request.form['exp_month'],
                                 'cc_year': request.form['exp_year'],
                                 'cc_cvv': request.form['cvv'],
                                 'amount': prod['init_price']*int(request.form['quantity']),
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
    else: #### its not those shitty ones, lets try nmi directly? ####
        try:
            mailservs = models.Smtpserver.objects(storeid=request.form.get('storeid'))[0]
        except:
            mailservs = models.Smtpserver.objects()[0]
	if request.form.get('quantity') == '':
		prod_q = 1
	else:
		prod_q = int(request.form['quantity'])
        try:
            chosen = nmiSelect(request.form['pid'], quantity=prod_q)
            prod = chosen['prod']
            nmiaccount = chosen['nmi']
        except:
            return jsonify({"success": False, "cc_response": "invalid product id"})
        if prod_q > 1:
            prodname = prod['name'] + " x"+str(prod_q)
            prodamount = float(prod['init_price']*prod_q)
        else:
            prodname = prod['name']
            prodamount = float(prod['init_price'])
        process = processing.NMI({'cc_number': newcard['card_number'],
                                 'cc_exp': newcard['exp_month']+newcard['exp_year'],
                                 'cc_cvv': newcard['ccv'],
                                 'amount': prodamount,
                                 'fname': oldguy['fname'],
                                 'lname': oldguy['lname'],
                                 'address': newcard['billing_address1'],
                                 'city': newcard['billing_city'],
                                 'state': newcard['billing_state'],
                                 'postal': str(newcard['billing_zipcode']),
                                 'email': oldguy['email'],
                                 'ip': remoteaddr}, nmiaccount.username, nmiaccount.password, nmiaccount.url).process()
        if prod['salestype'] == 'trial':
            future = datetime.datetime.now() + datetime.timedelta(days=prod['rebilldays'])
            x = models.Rebill(card=str(newcard.id), customer=str(oldguy.id), pid=request.form['pid'], date=future.strftime("%d/%m/%Y"), affid=request.form.get('affid'), retrynum=0, nmi_id=str(nmiaccount['id']))
            x.save()
        sm = tMail(mailservs['host'], mailservs['port'])
        sm.login(mailservs['username'], mailservs['password'], oldguy['email'])
        with open(os.path.join('emails', mailservs['theme'], 'order.html')) as fd:
            macros = {'fname': oldguy['fname'],
                      'lname': oldguy['lname'],
                      'bill_address': newcard['billing_address1'],
                      'bill_city': newcard['billing_city'],
                      'bill_state': newcard['billing_state'],
                      'bill_zip': newcard['billing_zipcode'],
                      'email': oldguy['email'],
                      'ip': remoteaddr,
                      'prod': prodname,
                      'total': str(prodamount),
                      'ccnum': ('*'*12)+newcard['card_number'][-4:]}
            email = fd.read()
            for x in macros.keys():
                email = email.replace("{"+x+"}", macros[x])
        sm.send(email)
    neworder = models.Order(creditcard=str(newcard.id), products=request.form['pid'], tracking=request.form['uniqid'], affid=request.form.get('affid'), order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
    neworder.save()
    visid = "didnt convert"
    if process.success:
      oldvisitor = models.Visitor.objects(uniqid=request.form['uniqid'], remoteaddr=remoteaddr, conversion=False)[0]
      oldvisitor['conversion'] = True
      oldvisitor['convert'] = request.form['pid']
      oldvisitor.save()
      visid = str(oldvisitor.id)
    oldguy['card'] = str(newcard.id)
    oldguy['order_time'] = datetime.datetime.now()
    oldguy.save()
    return jsonify({"card": str(newcard.id), "cc_response": process.raw_response, "success": process.success, "order": (process.orderid if processor == "ucrm" else str(neworder.id)), "visitor": visid})

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
                                 'billingsame': 'no',
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
            prod = models.Product.objects(id= request.form['pid'])[0]
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
        try:
            mailservs = models.Smtpserver.objects(storeid=request.form.get('storeid'))[0]
        except:
            mailservs = models.Smtpserver.objects()[0]
        try: #### its not those shitty ones, lets try nmi directly? ####
            prod = models.Product.objects(id= request.form['pid'])[0]
        except:
            return jsonify({"success": False, "cc_response": "invalid product id"})
        if request.form.get('quantity') == '':
            prodname = prod['name']
            prodamount = float(prod['init_price'])
        elif int(request.form['quantity']) > 1:
            prodname = prod['name'] + " x"+request.form['quantity']
            prodamount = float(prod['init_price']*int(request.form['quantity']))
        else:
            prodname = prod['name']
            prodamount = float(prod['init_price'])
        nmiaccount = models.NMIAccount.objects(id=processor)[0]
        process = processing.NMI({'cc_number': oldcard['card_number'],
                                 'cc_exp': oldcard['exp_month']+oldcard['exp_year'],
                                 'cc_cvv': oldcard['ccv'],
                                 'amount': prodamount,
                                 'fname': oldguy['fname'],
                                 'lname': oldguy['lname'],
                                 'address': oldcard['billing_address1'],
                                 'city': oldcard['billing_city'],
                                 'state': oldcard['billing_state'],
                                 'postal': str(oldcard['billing_zipcode']),
                                 'email': oldguy['email'],
                                 'ip': remoteaddr}, nmiaccount.username, nmiaccount.password, nmiaccount.url).process()
        if prod['salestype'] == 'trial':
            future = datetime.datetime.now() + datetime.timedelta(days=prod['rebilldays'])
            x = models.Rebill(card=str(oldcard.id), customer=str(oldguy.id), pid=request.form['pid'], date=future.strftime("%d/%m/%Y"), affid=request.form.get('affid'))
            x.save()
    neworder = models.Order(creditcard=str(oldcard.id), products=request.form['pid'], tracking=request.form['uniqid'], affid=request.form.get('affid'), order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
    neworder.save()
    return jsonify({"card": str(oldcard.id), "cc_response": process.raw_response, "success": process.success, "order": (process.orderid if processor == "ucrm" else str(neworder.id))})

if __name__=="__main__":
  app.run(host="0.0.0.0", port=55555, debug=True)
