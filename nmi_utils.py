import models
from random import randint

def nmiSelect(prod_id, curr_id=False, quantity=1):
	totalnmi = models.NMIAccount.objects(prod_id=str(prod_id)).count()
	if curr_id == False:
		n = models.NMIAccount.objects(prod_id=str(prod_id))
        	x = n.limit(1).skip(randint(0,n.count()-1)).next()
		is_rebill = False
	else:
		x = models.NMIAccount.objects(id=curr_id).skip(0).limit(1)[0]
		is_rebill = True
	y = models.Product.objects(id=prod_id).limit(1)[0]
	prod_price = (y['rebill_price'] if is_rebill else y['init_price']) * quantity
	tried = 0
	while (x['month_charged'] + prod_price) > x['month_limit']:
		print "[!!] NMI account at cap: "+str(x['id'])+"\n"+x['username']+"\n\n"
		n = models.NMIAccount.objects(prod_id=str(prod_id))
        	x = n.limit(1).skip(randint(0,n.count()-1)).next()
		tried += 1
		if tried > int(totalnmi*1.5):
			print "CANT FIND NMI ACCOUNT! WE NEED MOAR CAP!!!"
			raise IndexError
	print "[ok] Using NMI account: "+str(x['id'])
	print "month-to-date: "+ str(x['month_charged'])
	x['month_charged'] += prod_price
	print "charged: "+str(prod_price)
	print "new total: "+str(x['month_charged'])+"\n"
	x.save()
	return {'nmi':x, 'prod':y}

if __name__ == "__main__":
	testnmi = models.NMIAccount.objects(username="demo").skip(0).limit(1)[0]
	print "resetting demo acount"
	testnmi['month_charged'] = 0.0
	testnmi['month_limit'] = 100.0
	testnmi.save()
	try:
		for z in range(100):
			print str(z+1)
			nmiSelect(testnmi['prod_id'])
	except IndexError:
		print "everything functions correctly..."