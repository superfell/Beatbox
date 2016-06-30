# demonstration of using the BeatBox library to call the sforce API, this will update your chatter status

from __future__ import print_function
import os
import sys
import beatbox
import xmltramp
import datetime

sf = beatbox._tPartnerNS
svc = beatbox.Client()
if 'SF_SANDBOX' in os.environ:
    svc.serverUrl = svc.serverUrl.replace('login.', 'test.')

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("usage is setstatus.py <username> <password> <new status>")
    else:
        loginResult = svc.login(sys.argv[1], sys.argv[2])
        print("welcome " + str(loginResult[sf.userInfo][sf.userFullName]))
        user = { 'type' : 'FeedItem',
                 'parentId'     : str(loginResult[sf.userId]),
                 'body'         : sys.argv[3] }
        r = svc.create(user)
        if (str(r[sf.success]) == 'false'):
            print("error updating status:" + str(r[sf.errors][sf.statusCode]) + ":" + str(r[sf.errors][sf.message]))
        else:
            print("success!")
