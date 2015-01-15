from suds.client import Client
if __name__=="__main__":
	from random import randint

c = Client("https://secure-wms.com/webserviceexternal/contracts.asmx?WSDL")
l = c.factory.create("ExternalLoginData")
l.ThreePLKey = "{a240f2fb-ff00-4a62-b87b-aecf9d5123f9}"
l.Login = "zmgllc"
l.Password = "zmgllc"
l.FacilityID = 2

def stripIt(o, rlvl=1):
	for a in o:
		if a[1] == None:
			#print (">"*rlvl)+a[0]
			o.__delattr__(a[0])
		elif type(o[a[0]]) == type(o):
			stripIt(o[a[0]], rlvl+1)
	return o

def ShipOrder(refnum, name, address1, address2, city, state, postal, country, products, notes="Order sent from TRM"):
	#products = [{'sku': 'Louv1', 'qty': 1}, {'sku': 'Louv2', 'qty': 1}]
	o = c.factory.create("Order")
	o.TransInfo.ReferenceNum = refnum
	#o.TransInfo.EarliestShipDate = "1/2/30"
	o.ShipTo.Name = name
	#o.ShipTo.CompanyName = "ZMG LLC"
	o.ShipTo.Address.Address1 = address1
	o.ShipTo.Address.Address2 = address2
	o.ShipTo.Address.City = city
	o.ShipTo.Address.State = state
	o.ShipTo.Address.Zip = postal
	o.ShipTo.Address.Country = country
	o.ShippingInstructions.Carrier = "USPS"
	o.ShippingInstructions.Mode = "First Class Mail"
	o.ShippingInstructions.BillingCode = "Prepaid"
	#o.ShippingInstructions.Account = "123456789"
	o.Notes = notes
	il = []
	for x in products:
		i = c.factory.create("OrderLineItem")
		i.SKU = x['sku']
		i.Qty = x['qty']
		il += [stripIt(i)]
	
	aoi = c.factory.create("ArrayOfOrderLineItem")
	aoi.OrderLineItem = il
	o.OrderLineItems = [stripIt(aoi)]
	
	aoo = c.factory.create("ArrayOfOrder")
	aoo.Order = [stripIt(o)]
	
	print aoo
	
	#try:
	c.service.CreateOrders(l, aoo)
	#except:
	#print c.last_sent()

if __name__=="__main__":
	ShipOrder("TEST"+str(randint(1000,9999), "Testing McFixinStuff", "5 w seventh wei", None, "Burbank", "CA", "90001", "US", [{'sku': 'Louv1', 'qty': 1}, {'sku': 'Louv2', 'qty': 1}], "Test order. Do not ship.")
