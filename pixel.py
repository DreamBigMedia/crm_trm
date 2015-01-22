from flask import request, jsonify, Flask
from nmi_utils import nmiSelect
import processing, models, json, datetime, os.path, logging

@app.route("/pixel/<postback>")
def postback_url(postback):
 if models.Visitor.objects(uniqid=postback).count() >0:
  converted_visitor = models.Visitor.objects(uniqid=postback)[0]
  converted_visitor.conversion=True
  converted_visitor.save()
  return str(converted_visitor.id)
