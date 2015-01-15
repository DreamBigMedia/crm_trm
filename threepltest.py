from suds.client import Client

c = Client("https://secure-wms.com/webserviceexternal/contracts.asmx?WSDL")

o1 = c.factory.create("Order")
def stripIt(o, rlvl=1):
	for a in o:
		if a[1] == None:
			#print (">"*rlvl)+a[0]
			o.__delattr__(a[0])
		elif type(o[a[0]]) == type(o):
			stripIt(o[a[0]], rlvl+1)
	return o

l = c.factory.create("ExternalLoginData")
l.ThreePLKey = "{a240f2fb-ff00-4a62-b87b-aecf9d5123f9}"
l.Login = "zmgllc"
l.Password = "zmgllc"
l.FacilityID = 2

o = c.factory.create("Order")
o.TransInfo.ReferenceNum = "35t321t"
#o.TransInfo.EarliestShipDate = "1/2/30"
o.ShipTo.Name = "Test DoNotShip"
o.ShipTo.CompanyName = "ZMG LLC"
o.ShipTo.Address.Address1 = "217 w alamedia ave"
o.ShipTo.Address.Address2 = "#201"
o.ShipTo.Address.City = "Burbank"
o.ShipTo.Address.State = "CA"
o.ShipTo.Address.Zip = "90001"
o.ShipTo.Address.Country = "US"
o.ShippingInstructions.Carrier = "USPS"
o.ShippingInstructions.Mode = "Ground"
o.ShippingInstructions.BillingCode = "FreightCollect"
o.ShippingInstructions.Account = "123456789"
o.Notes = "Test order - CRM development"

i = c.factory.create("OrderLineItem")
i.SKU = "Louv1"
i.Qty = 1

aoi = c.factory.create("ArrayOfOrderLineItem")
aoi.OrderLineItem = [stripIt(i)]
o.OrderLineItems = [stripIt(aoi)]

aoo = c.factory.create("ArrayOfOrder")
aoo.Order = [stripIt(o)]

#try:
c.service.CreateOrders(l, aoo)
#except:
print c.last_sent()
