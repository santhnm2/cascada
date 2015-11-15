class Post(object):

	def __init__(self, text, indent, postid, parentid, user, assignmentName):
		self.text = text
		self.indent = indent
		self.postid = postid
		self.parentid = parentid
		self.user = user;
		self.assignmentName = assignmentName

	def getPostId(self):
		return self.postid

	def getParentId(self):
		return self.parentid

	def getAssignmentName(self):
		return self.assignmentName

	def getPostText(self):
		return self.text

	def getUser(self):
		return self.user;

	def getIndent(self):
		return self.indent*80

	def getAuthorIndent(self):
		return self.indent*80+10

	def getColor(self):
		if self.indent == 0:
			return "#F5A9A9"
		elif self.indent == 1:
			return "#F5BCA9"
		elif self.indent == 2:
			return "#F3E2A9"
		elif self.indent == 3:
			return "#BCF5A9"
		else:
			return "#2ECCFA"