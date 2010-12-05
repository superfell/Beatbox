# demonstration of using the BeatBox library to call the sforce API, this will update your chatter status

import sys
import beatbox
import xmltramp
import datetime

sf = beatbox._tPartnerNS
svc = beatbox.Client()

if __name__ == "__main__":

	if len(sys.argv) != 4:
		print "usage is setstatus.py <username> <password> <new status>"
	else:
		loginResult = svc.login(sys.argv[1], sys.argv[2])
		print "welcome " + str(loginResult[sf.userInfo][sf.userFullName])
		user = { 'type' : 'User',
				 'id'   : str(loginResult[sf.userId]),
				 'currentStatus' : sys.argv[3] }
		r = svc.update(user)
		if (str(r[sf.success]) == 'false'):
			print "error updating status:" + str(r[sf.errors][sf.statusCode]) + ":" + str(r[sf.errors][sf.message])
		else:
			print "success!"
		