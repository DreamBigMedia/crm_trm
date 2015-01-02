from flask import request, jsonify, Flask
import processing, models, json, datetime

app = Flask(__name__)

@app.route("/update/<collection>", methods="POST")
def updateTable(collection, column, value):
  if request.form.get('id') != '':
   a = getattr(models, collection.title()).objects(id=request.form['id'])[0]
   xyz = {}
   for x in y:
    if x == 'id':
     continue
    a[x] = request.form[x]
    xyz[x] = str(a[x])
  else:
   xyz = {}
   for x in y:
    if x == 'id':
     continue
    xyz[x] = request.form[x]
   a = getattr(models, collection.title())(**xyz)
  a.save()
  return jsonify(xyz)

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

if __name__=="__main__":
  app.run(host="0.0.0.0", port=30303, debug=True)
