import models
demo = models.NMIAccount(name="nmidemo", url="https://secure.networkmerchants.com/api/transact.php", username="demo", password="password")
demo.save()
print repr(demo)
print "NMI demo account id: "+str(demo.id)

