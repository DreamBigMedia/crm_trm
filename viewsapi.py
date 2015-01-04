from flask import request, jsonify, Flask, render_template, redirect
import processing, models, json, datetime

app = Flask(__name__)

@app.errorhandler(404)
def home(e):
 return redirect("/trm/product/$natural/0/20", code=302)

@app.route("/trm/<collection>/<sortmethod>/<start>/<num>")
def trm(**demArgs):
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
  return str(getattr(models, collection.title()).objects(id=thatid)[0].delete())

@app.route("/one/<collection>/<column>/<value>")
def getOrder(collection, column, value):
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
    xyz[x] = str(y[x])
   z[c] = xyz
   c += 1
 return jsonify(z)

@app.route("/columns/<collection>")
def getColumns(collection):
 x = getattr(models, collection.title()).objects().limit(1)[0]
 z = {}
 c = 0
 for y in x:
  z[c] = y
  c += 1
 return jsonify(z)

@app.route("/get/affid/<affid>")
def getByAffid(affid):
 visitors = {'notengage': {'bought': models.Visitor.objects(c1=affid, engage=False, conversion=True).count, 'notbought': models.Visitor.objects(c1=affid, engage=False, conversion=False).count},
             'engage': {'bought': models.Visitor.objects(c1=affid, engage=True, conversion=True).count, 'notbought': models.Visitor.objects(c1=affid, engage=True, conversion=False).count}}
 return jsonify(visitors)
 

if __name__=="__main__":
  app.run(host="0.0.0.0", port=30303, debug=True)
