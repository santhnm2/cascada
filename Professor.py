class Professor(object):

	def __init__(self, name, email_address):
		self.name = name
		self.email_address = email_address

	def getName(self):
		return self.name

	def getEmailAddress(self):
		return self.email_address