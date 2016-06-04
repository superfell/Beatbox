# demonstration of using the BeatBox library to call the sforce API

import sys
import beatbox
import xmltramp
import datetime

sf = beatbox._tPartnerNS
svc = beatbox.Client()
beatbox.gzipRequest=False

class BeatBoxDemo:
	def login(self, username, password):
		self.password = password
		loginResult = svc.login(username, password)
		print("sid = " + str(loginResult[sf.sessionId]))
		print("welcome " + str(loginResult[sf.userInfo][sf.userFullName]))
	
	def getServerTimestamp(self):
		print("\ngetServerTimestamp " + svc.getServerTimestamp())
	
	def describeGlobal(self):
		print("\ndescribeGlobal")
		dg = svc.describeGlobal()
		for t in dg[sf.sobjects:]:
			print(str(t[sf.name]) + " \t " + str(t[sf.label]))

	def describeTabs(self):
		print("\ndescribeTabs")
		dt = svc.describeTabs()
		for t in dt:
			print(str(t[sf.label]))

	def describeSearchScopeOrder(self):
		print("\ndescribeSearchScopeOrder")
		types = svc.describeSearchScopeOrder()
		for t in types:
			print("\t" + str(t[sf.name]) + " : " + str(t[sf.keyPrefix]))
			
	def dumpQueryResult(self, qr):
		print("query size = " + str(qr[sf.size]))
	
		for rec in qr[sf.records:]:
			print(str(rec[0]) + " : " + str(rec[2]) + " : " + str(rec[3]))
	
		if (str(qr[sf.done]) == 'false'):
			print("\nqueryMore")
			qr = svc.queryMore(str(qr[sf.queryLocator]))
			for rec in qr[sf.records:]:
				print(str(rec[0]) + " : " + str(rec[2]) + " : " + str(rec[3]))

	def query(self):
		print("\nquery"			)
		qr = svc.query("select Id, Name from Account")
		self.dumpQueryResult(qr)

	def queryAll(self):
		print("\nqueryAll")
		qr = svc.queryAll("select id, isDeleted from Account")
		self.dumpQueryResult(qr)
		
	def search(self):				
		print("\nsearch")
		sr = svc.search("find {Apple*} in all fields")
		for rec in sr[sf.searchRecords:]:
			r = rec[sf.record]
			print(str(r[0]) + "\t: " + str(r[2]))

	def upsert(self):
		print("\nupsert")
		t = { 'type': 'Task', 
			  'ChandlerId__c': '12345', 
			  'subject': 'BeatBoxTest updated', 
			  'ActivityDate' : datetime.date(2006,2,20) }
	
		ur = svc.upsert('ChandlerId__c', t)
		print(str(ur[sf.success]) + " -> " + str(ur[sf.id]))
	
		t = { 	'type': 'Event', 
			'ChandlerId__c': '67890', 
			'durationinminutes': 45, 
			'subject': 'BeatBoxTest', 
			'ActivityDateTime' : datetime.datetime(2006,2,20,13,30,30),
			'IsPrivate': False }
		ur = svc.upsert('ChandlerId__c', t)
		if str(ur[sf.success]) == 'true':
			print("id " + str(ur[sf.id]))
		else:
			print("error " + str(ur[sf.errors][sf.statusCode]) + ":" + str(ur[sf.errors][sf.message]))

	def update(self):
		print("\nupdate")
		a = { 'type': 'Account',
			  'Id':   self.__idToDelete,
			  'Name': 'BeatBoxBaby',
			  'NumberofLocations__c': 123.456 }
		sr = svc.update(a)

		if str(sr[sf.success]) == 'true':
			print("id " + str(sr[sf.id]))
		else:
			print("error " + str(sr[sf.errors][sf.statusCode]) + ":" + str(sr[sf.errors][sf.message]))
    	
	def create(self):
		print("\ncreate")
		a = { 'type': 'Account',
			'Name': 'New Account',
			'Website': 'http://www.pocketsoap.com/' }
		sr = svc.create([a])

		if str(sr[sf.success]) == 'true':
			print("id " + str(sr[sf.id]))
			self.__idToDelete = str(sr[sf.id])
		else:
			print("error " + str(sr[sf.errors][sf.statusCode]) + ":" + str(sr[sf.errors][sf.message]))
    
    
	def getUpdated(self):
		print("\ngetUpdated")
		updatedIds = svc.getUpdated("Account", datetime.datetime.today()-datetime.timedelta(1), datetime.datetime.today()+datetime.timedelta(1))
		self.__theIds = []
		for id in updatedIds[sf.ids:]:
			print("getUpdated " + str(id))
			self.__theIds.append(str(id))

	def delete(self):
		print("\ndelete")
		dr = svc.delete(self.__idToDelete)
		if str(dr[sf.success]) == 'true':
			print("deleted id " + str(dr[sf.id]))
		else:
			print("error " + str(dr[sf.errors][sf.statusCode]) + ":" + str(dr[sf.errors][sf.message]))
	
	def undelete(self):
		print("\nundelete")
		dr = svc.undelete(self.__idToDelete)
		if (str(dr[sf.success])) == 'true':
			print("undeleted id " + str(dr[sf.id]))
		else:
			print("error " + str(dr[sf.errors][sf.statusCode]) + ":" + str(dr[sf.errors][sf.message]))

	def getDeleted(self):
		print("\ngetDeleted")
		drs = svc.getDeleted("Account", datetime.datetime.today()-datetime.timedelta(1), datetime.datetime.today()+datetime.timedelta(1))
		print("latestDate Covered : " + str(drs[sf.latestDateCovered]))
		for dr in drs[sf.deletedRecords:]:
			print("getDeleted " + str(dr[sf.id]) + " on " + str(dr[sf.deletedDate]))

	def retrieve(self):
		print("\nretrieve")
		accounts = svc.retrieve("id, name", "Account", self.__theIds)
		for acc in accounts:
			if len(acc._dir) > 0:
				print(str(acc[beatbox._tSObjectNS.Id]) + " : " + str(acc[beatbox._tSObjectNS.Name]))
			else:
				print("<null>")
			
			
	def getUserInfo(self):			
		print("\ngetUserInfo")
		ui = svc.getUserInfo()
		print("hello " + str(ui[sf.userFullName]) + " from " + str(ui[sf.organizationName]))
	
	def resetPassword(self):
		ui = svc.getUserInfo()
		print("\nresetPassword")
		pr = svc.resetPassword(str(ui[sf.userId]))
		print("password reset to " + str(pr[sf.password]))
	
		print("\nsetPassword")
		svc.setPassword(str(ui[sf.userId]), self.password)
		print("password set back to original password")
	
	def convertLead(self):
		print("\nconvertLead")
		lead = { 'type' : 'Lead', 
				 'LastName' : 'Fell', 
				 'Company' : '@superfell' }
		leadId = str(svc.create(lead)[sf.id])
		print("created new lead with id " + leadId)
		convert = { 'leadId' : leadId,
					'convertedStatus' : 'Closed - Converted',
					'doNotCreateOpportunity' : 'true' }
		res = svc.convertLead(convert)
		print("converted lead to contact with Id " + str(res[sf.contactId]))
					
	def describeSObjects(self):
		print("\ndescribeSObjects(Account)")
		desc = svc.describeSObjects("Account")
		for f in desc[sf.fields:]:
			print("\t" + str(f[sf.name]))

		print("\ndescribeSObjects(Lead, Contact)")
		desc = svc.describeSObjects(["Lead", "Contact"])
		for d in desc:
			print(str(d[sf.name]) + "\n" + ( "-" * len(str(d[sf.name]))))
			for f in d[sf.fields:]:
				print("\t" + str(f[sf.name]))
		
	def describeLayout(self):		
		print("\ndescribeLayout(Account)")
		desc = svc.describeLayout("Account")
		for layout in desc[sf.layouts:]:
			print("sections in detail layout " + str(layout[sf.id]))
			for s in layout[sf.detailLayoutSections:]:
				print("\t" + str(s[sf.heading]))
			
			
			
if __name__ == "__main__":

	if len(sys.argv) != 3:
		print("usage is demo.py <username> <password>")
	else:
		demo = BeatBoxDemo()
		demo.login(sys.argv[1], sys.argv[2])
		demo.getServerTimestamp()
		demo.getUserInfo()
		demo.convertLead()
		#demo.resetPassword()
		demo.describeGlobal()
		demo.describeSearchScopeOrder()
		demo.describeTabs()
		demo.describeSObjects()
		demo.describeLayout()
		demo.query()
		demo.upsert()
		demo.create()
		demo.update()
		demo.getUpdated()
		demo.delete()
		demo.getDeleted()
		demo.queryAll()
		demo.undelete()
		demo.retrieve()
		demo.search()
		
