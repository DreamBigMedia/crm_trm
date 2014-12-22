import models, datetime
from flask import request, render_template,jsonify,json

from mainapp import app
@app.route('/track/<int:vid>')
def track_hit():
 v1 = request.args.get('vid','',type=int)
 c1 = request.args.get('c1','', type=str)
 c2 = request.args.get('c2','', type=str)
 c3 = request.args.get('c3','',type=str)
 c4 = request.args.get('c4','',type = str)
 c5 = request.args.get('c5','',type = str)
 trafficsource = request.args.get('t1','unknown',type=str)
 l1 = request.args.get('l1','unknown',type= str)
 useragent = request.headers.get('User-Agent','unknown browser',type= str)
 visitor = models.Visitor(c1= c1, c2=c2,c3= c3, c4 = c4,c5=c5, trafficsource = trafficsource,
                          conversion=False,engage=False,useragent=useragent,convert=False,lander=l1).save()
 vi = visitor.id
 return jsonify({'visitor_id':vi})




@app.route('/engage/')
def engage_hit():
 visitor = models.Visitor.objects.get(id=request.args.get('vid'))
 visitor.engaged=True
 visitor.save()
 vi = visitor.id
 return jsonify({'visitor_id':vi})
