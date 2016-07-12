# demonstration of using the BeatBox library to authentication a portal user

from __future__ import print_function
import os
import sys
import beatbox

sf = beatbox._tPartnerNS
svc = beatbox.Client()
if 'SF_SANDBOX' in os.environ:
    svc.serverUrl = svc.serverUrl.replace('login.', 'test.')


class BeatBoxDemo:
    def login(self, username, password, orgId, portalId):
        loginResult = svc.portalLogin(username, password, orgId, portalId)
        print(str(loginResult[sf.sessionId]))

if __name__ == "__main__":

    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("usage is login_portal.py <username> <password> <orgId> {portalId}")
    else:
        demo = BeatBoxDemo()
        portalId = None
        if len(sys.argv) > 4:
            portalId = sys.argv[4]
        demo.login(sys.argv[1], sys.argv[2], sys.argv[3], portalId)
