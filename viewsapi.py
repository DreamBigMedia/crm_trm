from flask import request, jsonify, Flask, render_template, redirect, send_from_directory
from urlparse import parse_qs
import processing, models, json, datetime, hashlib, logging, requests

app = Flask(__name__)

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('views.log')
logger.addHandler(handler)

# Also add the handler to Flask's logger for cases
#  where Werkzeug isn't used as the underlying WSGI server.
app.logger.addHandler(handler)

@app.route("/sample/affid/thing")
def sample():
	return jsonify({'visitors': {'engage': {'notbought': 5, 'bought': 3}, 'notengage': {'notbought': 10, 'bought': 1}}, 'products': {'549e2aba09d024031841af28': {'type': 'trial', 'name': 'Triangle Product', 'sales': 3}}})

@app.route("/sample/stats/<start>/<end>/<affid>")
def samplestats(start, end, affid):
	d1=datetime.datetime.strptime(start, '%m-%d-%Y')
	d2=datetime.datetime.strptime(end, '%m-%d-%Y')
	return jsonify({"": {}, "id_1/id_2/id_3": {"clicks": 14, "partials": 2, "sales": 1, "upsales": 0}, "strausburg//None": {"clicks": 209, "partials": 93, "sales": 66, "upsales": 33}, "hamilton//strange": {"clicks": 209, "partials": 93, "sales": 66, "upsales": 33}})

@app.route('/stats/<path:filename>')
def send_foo(filename):
    if loggedIn() == False:
     return redirect('/login')
    return send_from_directory('./static_views/', filename)

loggedinusers = {}
def loggedIn():
    cookie = request.cookies.get('lgnCookie')
    if cookie in loggedinusers.keys():
      return loggedinusers[cookie]
    else:
      return False

passwd_salt = "aougSAJFISAhg4%()*&DvTriangle%IHclmdojfby7900000iamgodbitchdonthackthis_illkillyou"
def logIn(user, passwd):
  global loggedinusers
  pwhash = hashlib.md5(passwd+"\\"+user+"\\"+passwd_salt).hexdigest()
  x = models.Affiliate.objects(username=user)
  if x.count() > 0:
   y = x[0]
   if y['pwhash'] == pwhash:
    datcookie = user+"\\\\"+hashlib.md5(pwhash+user).hexdigest()
    loggedinusers[datcookie] = {'username': y['username'], 'affid':y['affid'], 'displayname': y['displayname'], 'loggedin': True}
    return datcookie
  return False

def addUser(user, passwd, affid = None, displayname=None):
 if displayname==None:
  displayname = user
 if affid==None:
  affid = user
 x = models.Affiliate(username = user, pwhash = hashlib.md5(passwd+"\\"+user+"\\"+passwd_salt).hexdigest(), affid=affid, displayname=displayname).save()

@app.errorhandler(404)
def home(e):
 return redirect("/login", code=302)

@app.route("/login", methods=["GET", "POST"])
def loginPage():
 li = loggedIn()
 if li != False:
  if li['loggedin'] == True:
   return redirect("/trm/product/$natural/0/50")
 if request.method=="POST":
  x = logIn(request.form['username'], request.form['passwd'])
  if x != False: 
   r = app.make_response(redirect("/stats/index.html"))
   r.set_cookie("lgnCookie", value=x)
   return r
  return "<html><head><title>WRONG PASSWORD quit haxn bruh</title><script type='text/javascript'>setTimeout(function(){window.location.href='/login';}, 10000);</script></head><body>That wasnt the password...quit haxn bruh</body></html>"
 return "<html><head><title>&nbsp;:&nbsp;TRM Login&nbsp;:&nbsp;</title></head><body><form method='POST' action='/login'>Email: <input type='text' name='username'><br>Passwd: <input type='password' name='passwd'><br><input type='submit' value='What my stats?'></form></body></html>"

@app.route("/trm/<collection>/<sortmethod>/<start>/<num>")
def trm(**demArgs):
 if loggedIn() == False:
  return redirect('/login')
 demArgs['displayname'] = loggedIn()['displayname']
 return render_template('view.html', **demArgs)

def mongoconvert(table, data):
 retval = {}
 for x in data:
  if table._fields[x].__class__.__name__ == "IntField":
    retval[x] = int(data[x])
  elif table._fields[x].__class__.__name__ == "BooleanField":
    retval[x] = bool(data[x])
  elif table._fields[x].__class__.__name__ == "FloatField":
    retval[x] = float(data[x])
  elif table._fields[x].__class__.__name__ == "ObjectIdField":
    continue
  else:
    retval[x] = data[x]
 return retval

@app.route("/update/<collection>", methods=["POST"])
def updateTable(collection):
  if loggedIn() == False:
   return redirect('/login')
  b = getattr(models, collection.title())
  print repr(request.form.get('id'))
  if request.form.get('id') != '':
   a = b.objects(id=request.form['id'])[0]
   xyz = {}
   zyx = mongoconvert(b, request.form)
   for x in a:
    print repr(x)
    if x == 'id':
     continue
    a[x] = zyx[x]
    xyz[x] = str(a[x])
  else:
   xyz = {}
   zyx = mongoconvert(b, request.form)
   for x in request.form:
    print repr(x)
    if x == 'id':
     continue
    xyz[x] = zyx[x]
   a = b(**xyz)
  a.save()
  return jsonify(xyz)

@app.route("/remove/<collection>/<thatid>")
def removeRow(collection, thatid):
  if loggedIn() == False:
   return redirect('/login')
  return str(getattr(models, collection.title()).objects(id=thatid)[0].delete())

@app.route("/stats/daterange/<start>/<end>/<affid>")
def stateDaterange(start, end, affid):
 if loggedIn() == False:
  return redirect('/login')
 if affid == "me":
  affid = loggedIn()['affid']
 d1=datetime.datetime.strptime(start, '%m-%d-%Y')
 d2=datetime.datetime.strptime(end, '%m-%d-%Y')
 print str(d1)+"\t"+str(d2)
 w = models.Visitor.objects(affid=affid, visit_date__gte=d1, visit_date__lte=d2)
 u = {'': {}}
 for v in w:
  cval = "/".join([str(v['c1']), str(v['c2']), str(v['c3'])])
  if cval not in u.keys():
   u[cval] = {'clicks': 0,'partials': 0,'sales': 0,'upsales': 0}
  u[cval]['clicks'] += 1
  if v['conversion']:
   u[cval]['sales'] += 1
   if v['upsell']:
    u[cval]['upsales'] += 1
  elif v['lead']:
   u[cval]['partials'] += 1
 return jsonify(u)


@app.route("/one/<collection>/<column>/<value>")
def getOrder(collection, column, value):
 if loggedIn() == False:
  return redirect('/login')
 xyz = {}
 y = getattr(models, collection.title()).objects(**{column: value})[0]
 for x in y:
  xyz[x] = str(y[x])
 return jsonify(xyz)

@app.route("/all/<collection>/<sortmethod>/<int:start>/<int:num>")
def getOrders(collection, sortmethod, start, num):
 x = getattr(models, collection.title()).objects().order_by(sortmethod).skip(start).limit(num)
 z = {}
 c = 0
 for y in x:
   xyz = {}
   for x in y:
    try:
     xyz[x] = str(y[x])
    except:
     xyz[x] = unicode(y[x], 'utf-8')
   z[c] = xyz
   c += 1
 return jsonify(z)

@app.route("/filter/<collection>/<sortmethod>/<int:start>/<int:num>/<query>")
def filterResult(collection, sortmethod, start, num, query):
 if loggedIn() == False:
  return redirect('/login')
 q_t = parse_qs(query)
 q = {}
 for x in q_t:
  try:
   if getattr(models, collection.title())()[x].__class__ == type(True):
    q_t[x][0] = bool(q_t[x][0])
  except:
   pass
  q[x] = q_t[x][0]
 x = getattr(models, collection.title()).objects(**q).order_by(sortmethod).skip(start).limit(num)
 z = {}
 c = 0
 for y in x:
   xyz = {}
   for x in y:
    try:
     xyz[x] = str(y[x])
    except:
     xyz[x] = unicode(y[x], 'utf-8')
   z[c] = xyz
   c += 1
 return jsonify(z)

@app.route("/columns/<collection>")
def getColumns(collection):
 if loggedIn() == False:
  return redirect('/login')
 x = getattr(models, collection.title()).objects().limit(1)[0]
 z = {}
 c = 0
 for y in x:
  z[c] = y
  c += 1
 return jsonify(z)

@app.route("/get/affids")
def getAffids():
 if loggedIn() == False:
  return redirect('/login')
 aid = []
 for x in models.Affiliates.objects():
  aid += x['affid']
 return jsonify(aid)

@app.route("/get/affid/<affid>")
def getByAffid(affid):
 if loggedIn() == False:
  return redirect('/login')
 if affid == "me":
  affid = loggedIn()['affid']
 visitors = {'notengage': {'bought': models.Visitor.objects(c1=affid, engage=False, conversion=True).count(), 'notbought': models.Visitor.objects(c1=affid, engage=False, conversion=False).count()},
             'engage': {'bought': models.Visitor.objects(c1=affid, engage=True, conversion=True).count(), 'notbought': models.Visitor.objects(c1=affid, engage=True, conversion=False).count()}}
 orders = {}
 for x in models.Order.objects(affid=affid):
  if x['products'] not in orders.keys():
   try:
    orders[x['products']] = {'sales': 0,
                       'name': models.Product.objects(id=x['products'])[0]['name'],
                       'type': models.Product.objects(id=x['products'])[0]['salestype']}
   except:
    orders[x['products']] = {'sales': 0,
                       'name': x['products'],
                       'type': 'trial'}
  orders[x['products']]['sales'] += 1
 return jsonify({'products': orders, 'visitors': visitors})

#@app.route("/refund", methods=['GET', 'POST'])
def refund():
 if request.method == "POST":
  order = models.Order.objects(id=request.form['order_id'])[0]
  nmi = models.NMIAccount.objects(id=order['nmi_id'])[0]
  pdata = {'type': 'refund',
              'username': nmi['username'],
              'password': nmi['password'],
              'transactionid': order['tx_id']}
  return requests.post(nmi['gateway'], pdata).text
 return '<html><body><form method="POST">order id: <input type="text" name="order_id"><input type="submit" value="refund"></form></body></html>'

@app.route("/refund/<order_id>")
def refundOrder(order_id):
 order = models.Order.objects(id=order_id)[0]
 if order['refunded'] == True:
  return "<html><body>This order has already been refunded.<br><a href='javascript:window.history.back()'>Go back</a></body></html>"
 nmi = models.NMIAccount.objects(id=order['nmi_id'])[0]
 pdata = {'type': 'refund',
             'username': nmi['username'],
             'password': nmi['password'],
             'transactionid': order['tx_id']}
 retval = requests.post(nmi['url'], pdata).text
 order['refunded'] = True
 order.save()
 return "<html><body>"+retval+"<br><a href='javascript:window.history.back()'>Go back</a></body></html>"


if __name__=="__main__":
  app.run(host="0.0.0.0", port=30303, debug=True)
