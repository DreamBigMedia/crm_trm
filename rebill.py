import models, time, datetime, processing
from nmi_utils import nmiSelect, nmiCancel
from hashtag import ShipOrder

for x in models.Rebill.objects(date=time.strftime("%d/%m/%Y"), batched=False):
	oldcard = models.Creditcard.objects(id=x['card'])[0]
	oldguy = models.Customer.objects(id=x['customer'])[0]
	n = nmiSelect(x['pid'], x['nmi_id']) # get product and assign merchant account
	prod = n['prod']
	prodname = prod['name']
	prodamount = float(prod['rebill_price'])
	nmiaccount = n['nmi']
	print oldguy['fname']+"\t"+oldguy['lname']
	print oldcard['card_number'][:4]+('*'*8)+oldcard['card_number'][-4:]
	print oldcard['exp_month']+"/"+oldcard['exp_year']
	print oldcard['billing_address1'] # for cron output
	print oldcard['billing_city']+", "+oldcard['billing_state']+" "+str(oldcard['billing_zipcode'])
	print oldguy['email']
	process = processing.NMI({'cc_number': oldcard['card_number'], # charge them
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
	if process.success: # approved
		print "approved: "+str(process.success)+"\n" #schedule for next rebill date
		future = datetime.datetime.now() + datetime.timedelta(days=prod['rebilldays']-x['retrynum'])
		theretrynum = 0 # ship the item
		if ',' in prod['skus']:
			o=prod['skus'].split(',')
			p=[]
			for n in o:
				p += [{'sku':n, 'qty':prod_q}]
		else:
			p=[{'sku':prod['skus'], 'qty':prod_q}]
		ShipOrder("T5_"+str(neworder.id), oldguy['fname']+" "+oldguy['lname'], oldguy['ship_address1'], oldguy['ship_address2'], oldguy['ship_city'], oldguy['ship_state'], oldguy['ship_zipcode'], "US", p)
	else: # declined
		future = datetime.datetime.now() + datetime.timedelta(days=1) #retry tomorrow
		theretrynum = x['retrynum'] + 1
	if (x['retrynum'] >= MAX_RETRY_MAIL) and (not process.success):
		try: # we declined repeatedly...
			mailservs = models.Smtpserver.objects(storeid=str(nmiaccount['id']))[0]
		except:
			mailservs = models.Smtpserver.objects()[0]
		nmiCancel(str(prod['id']), str(nmiaccount['id'])) # take us out of monthly_willbill
		sm = tMail(mailservs['host'], mailservs['port']) # send "update your card" email
		sm.login(mailservs['username'], mailservs['password'], oldguy['email'])
		with open(os.path.join('emails', mailservs['theme'], 'updatecard.html')) as fd:
			macros = {'fname': oldguy['fname'], # set keywords
				'lname': oldguy['lname'],
				'email': oldguy['email'],
				'prod': prodname,
				'total': str(prodamount),
				'ccnum': ('*'*12)+newcard['card_number'][-4:],
				'decline_times': x['retrynum']}
			email = fd.read()
			for x in macros.keys(): # replace {KEYWORD} with macro value
				email = email.replace("{"+x+"}", macros[x])
			sm.send(email) # shoot it off
	x['batched'] = True
	x.save() # mark rebill as ran
	x = models.Rebill(card=str(oldcard.id), customer=str(oldguy.id), pid=x['pid'], date=future.strftime("%d/%m/%Y"), retrynum=theretrynum)
	x.save() # rebill them again
	neworder = models.Order(creditcard=str(oldcard.id), products=x['pid'], tracking="rebill", order_date=datetime.datetime.now(), success=process.success, server_response=process.str_response, nmi_id=x['nmi_id'])
	neworder.save() # record that transaction
