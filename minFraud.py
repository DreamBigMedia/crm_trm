import requests, hashlib

u = "https://minfraud.maxmind.com/app/ccv2r"
l = 'tMKcqO7GJUZC'

def minFraud(ip, bcity, bstate, bzip, bcountry, scity, sstate, szip, scountry, email, phone, cc, ua, accept_language, storeid):
	params = {'i':ip,
		'license_key': l,
		'city': bcity,
		'region': bstate,
		'postal': bzip,
		'country': bcountry,
		'shipCity': scity,
		'shipRegion': sstate,
		'shipPostal': szip,
		'shipCountry': scountry,
		'domain': email.split('@')[1],
		'custPhone': phone,
		'emailMD5': hashlib.md5(email).hexdigest(),
		'bin': cc[:6],
		'user_agent': ua,
		'accept_language': accept_language,
		'shopID': storid}
	x= requests.post(u, params).text
	retval = {}
	for y in x.split(';'):
		k,v = y.split('=')
		retval[k]=v
	return retval
