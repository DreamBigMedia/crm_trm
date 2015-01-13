import models
from random import randint

def nmiSelect(prod_id, curr_id=False):
	if curr_id == False:
		n = models.NMIAccount.objects(prod_id=str(prod_id)))
        	x = n.limit(1).skip(randint(0,n.count()-1)).next()
		is_rebill = False
	else:
		x = models.NMIAccount.objects(id=curr_id).limit(1)[0]
		is_rebill = True
	y = models.Product.objects(id=prod_id).limit(1)[0]
	while (x['month_charged'] + (y['rebill_price'] if is_rebill else y['init_price'])) > x['month_limit']:
		print "[!!] NMI account at cap: "+str(x['id'])+"\n"+x['username']+"\n\n"
		n = models.NMIAccount.objects(prod_id=str(prod_id)))
        	x = n.limit(1).skip(randint(0,n.count()-1)).next()
	print "[ok] Using NMI account: "+str(x['id'])
	print "month-to-date: "+ str(x['month_charged'])
	x['month_charged'] += y['rebill_price'] if is_rebill else y['init_price']
	print "charged: "+y['rebill_price'] if is_rebill else y['init_price']
	print "new total: "+x['month_charged']+"\n"
	x.save()
	return {'nmi':x, 'prod':y}
