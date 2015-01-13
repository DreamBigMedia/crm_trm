import models, time, datetime, processing


thisran = 0
currproc = 0
processors = models.NMIAccount.objects()
def processorCycle():
	global thisran
	global currproc
	if thisran >= processors[currproc].batchmax:
		currproc += 1
		thisran = 0
		while thisran >= processors[currproc].batchmax:
			currproc += 1
			if currproc >= len(processors):
				currproc = 0
				print "restarting from processor #0"
	if currproc >= len(processors):
		currproc = 0
		print "restarting from processor #0"
	thisran += 1
	print "processor: "+str(processors[currproc])
	return processors[currproc]

for x in models.Rebill.objects(date=time.strftime("%d/%m/%Y"), batched=False):
	oldcard = models.Creditcard.objects(id=x['card'])[0]
	oldguy = models.Customer.objects(id=x['customer'])[0]
	prod = models.Product.objects(id=x['pid'])[0]
	prodname = prod['name']
	prodamount = float(prod['rebill_price'])
	nmiaccount = models.NMIAccount.objects(prod_id=x['pid'])[0]
	print oldguy['fname']+"\t"+oldguy['lname']
	print oldcard['card_number'][:4]+('*'*8)+oldcard['card_number'][-4:]
	print oldcard['exp_month']+"/"+oldcard['exp_year']
	print oldcard['billing_address1']
	print oldcard['billing_city']+", "+oldcard['billing_state']+" "+str(oldcard['billing_zipcode'])
	print oldguy['email']
	process = processing.NMI({'cc_number': oldcard['card_number'],
				'cc_exp': oldcard['exp_month']+oldcard['exp_year'],
				'cc_cvv': oldcard['ccv'],
				'amount': prodamount,
				'fname': oldguy['fname'],
				'lname': oldguy['lname'],
				'address': oldcard['billing_address1'],
				'city': oldcard['billing_city'],
				'state': oldcard['billing_state'],
				'postal': str(oldcard['billing_zipcode']),
				'email': oldguy['email'],
				'ip': '127.0.0.1'}, nmiaccount.username, nmiaccount.password, nmiaccount.url).process()
	if process.success:
		print "approved: "+str(process.success)+"\n" #schedule for next rebill date
		future = datetime.datetime.now() + datetime.timedelta(days=prod['rebilldays']-x['retrynum'])
		theretrynum = 0
	else:
		future = datetime.datetime.now() + datetime.timedelta(days=1) #retry tomorrow
		theretrynum = x['retrynum'] + 1
	x['batched'] = True
	x.save()
	x = models.Rebill(card=str(oldcard.id), customer=str(oldguy.id), pid=x['pid'], date=future.strftime("%d/%m/%Y"), retrynum=theretrynum)
	x.save()
	neworder = models.Order(creditcard=str(oldcard.id), products=x['pid'], tracking="rebill", order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response)
	neworder.save()
