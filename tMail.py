import smtplib, socket

myhostname = socket.gethostname()

class tMail:
 def __init__(self, server, port):
  self.server = server
  self.port = port
 def login(self, username, password, to, fromaddr=None):
  if fromaddr==None:
   fromaddr = username+"@"+self.server
  self.username = username
  self.password = password
  self.fromaddr = fromaddr
  self.to = to
  self.sendmail = smtplib.SMTP(self.server, self.port)
  self.sendmail.ehlo_or_helo_if_needed()
  self.sendmail.login(self.username, self.password)
 def verify(self):
  if self.sendmail.verify(self.to)[0] == 250:
   return True
  else:
   return False
 def send(self, body):
  self.sendmail.sendmail(self.fromaddr, self.to, body)
