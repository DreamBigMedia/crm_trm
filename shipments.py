import requests
from settings import SETTINGS
usps_username = SETTINGS['usps']['username']
#usps_password = SETTINGS['usps']['password']
from ghetto_helpers import extract

def check_shipment(tracking_number,username,production=False):
  if(production==False):
    url = "http://production.shippingapis.com/ShippingAPITest.dll?API=TrackV2&XML=<TrackRequest USERID='"+username+"'>"
  else:
    url = "https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML=<TrackRequest USERID='"+username+"'>"
    
  url = url+"<trackID ID='"+tracking_number+"'></TrackID></TrackRequest>"
  resp = response.get(url)
  arrived = "Your item was delivered at"
  notice = "Notice left" 
  extracted = extract(resp.text,"<TrackSummary>","</TrackSummary>")
  if arrived in extracted or notice in extracted:
    return True
  else:
    return False
  
#  <TrackRequest USERID=”xxxxxxxx”>
#<TrackID ID="EJ123456780US"></TrackID>
#<TrackID ID="EJ123456781US"></TrackID>
#<TrackID ID="12345"></TrackID>
#</TrackRequest>

  
  
 
