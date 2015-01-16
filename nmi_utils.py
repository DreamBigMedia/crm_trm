import models
from random import randint

def nmiSelect(prod_id, curr_id=False, quantity=1):
	totalnmi = models.NMIAccount.objects(prod_id=str(prod_id)).count()
        y = models.Product.objects(id=prod_id).limit(1)[0]
	prod_price = 0.0
	extra_willbill = 0.0
	print "rebill willbill/month modifier: "+str(30.0/y['rebilldays'])
	if curr_id == False:
		n = models.NMIAccount.objects(prod_id=str(prod_id))
        	x = n.limit(1).skip(randint(0,n.count()-1)).next()
		if y['salestype'] == 'straight':
			prod_price = (y['init_price']*quantity)
			extra_willbill = prod_price
		else:
			prod_price = y['init_price']
			extra_willbill = y['init_price'] + (y['rebill_price'] *(30.0/y['rebilldays']))
		is_rebill = False
	else:
		x = models.NMIAccount.objects(id=curr_id).skip(0).limit(1)[0]
		prod_price = y['rebill_price']
		is_rebill = True
	tried = 0
	print str((x['month_willbill'] if y['salestype'] == 'trial' else x['month_charged']) + extra_willbill)+" > "+str(x['month_limit'])
	print str(x['month_willbill'] if y['salestype'] == 'trial' else x['month_charged'])
	print str(extra_willbill)
	while (x['month_willbill'] if y['salestype'] == 'trial' else x['month_charged']) + extra_willbill  > x['month_limit']:
		print "[!!] NMI account at cap: "+str(x['id'])+"\n"+x['username']+"\n\n"
		n = models.NMIAccount.objects(prod_id=str(prod_id))
        	x = n.limit(1).skip(randint(0,n.count()-1)).next()
		tried += 1
		if tried > int(totalnmi*1.5):
			print "CANT FIND NMI ACCOUNT! WE NEED MOAR CAP!!!"
			raise IndexError
	if (not is_rebill) and (y['salestype'] == 'trial'):
		x['month_willbill'] += y['rebill_price']*(30.0/y['rebilldays'])
	print "[ok] Using NMI account: "+str(x['id'])
	print "month-to-date: "+ str(x['month_charged'])
	x['month_charged'] += prod_price
	print "charged: "+str(prod_price)
	print "new total: "+str(x['month_charged'])
	print "MID monthly total: "+str(x['month_willbill'])+"\n"
	x.save()
	return {'nmi':x, 'prod':y}

def nmiCancel(prod_id, curr_id):
	x = models.NMIAccount.objects(id=curr_id)[0]
	y = models.Product.objects(id=prod_id)[0]
	print "Monthly willbill: "+str(x['month_willbill'])
	print y['name']+" willbill: "+str(y['rebill_price']*(30.0/y['rebilldays']))
	x['month_willbill'] -= y['rebill_price']*(30.0/y['rebilldays'])
	if x['month_willbill'] < 0:
		x['month_willbill']=0.0
		raise ValueError
	print "New willbill: "+str(x['month_willbill'])
	x.save()

if __name__ == "__main__":
	testnmi = models.NMIAccount.objects(username="demo").skip(0).limit(1)[0]
	print "resetting demo acount"
	testnmi['month_charged'] = 0.0
        testnmi['month_willbill'] = 0.0
	testnmi['month_limit'] = 25000.0
	testnmi.save()
	try:
		z=0
		while 1:
			print str(z+1)
			nmiSelect(testnmi['prod_id'])
			z +=1
	except IndexError:
		print "everything functions correctly..."
	try:
		z=0
                while 1:
                        print str(z+1)
                        nmiCancel(testnmi['prod_id'], str(testnmi['id']))
                        z +=1
        except ValueError:
                print "everything functions correctly..."
