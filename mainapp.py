from flask import Flask
app = Flask(__name__)
import orderapi, views, models, processing

if __name__=="__main__":
    orderapi.app.debug  = True
    orderapi.app.run(host='0.0.0.0', port=34203)
    views.app.debug = True
    views.app.run(host='0.0.0.0', port=42720)
