import models
try:
 demo = models.NMIAccount.objects(name="aloeveraorganic")[0]
except:
 demo = models.NMIAccount(name="aloeveraorganic", url="https://secure.networkmerchants.com/api/transact.php", username="aloeveraorganic1050", password="One1Two2!")
 demo.save()
print repr(demo)
print "NMI account id: "+str(demo.id)

