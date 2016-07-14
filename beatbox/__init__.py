from beatbox._beatbox import (                       # NOQA
        Client,  IterClient, SoapFaultError, islst,  # really public
        _tPartnerNS, _tSObjectNS, _envNs, _noAttrs,  # low level for a Python client
        XmlWriter, SoapWriter, SoapEnvelope,         # low level for tests
        )

__all__ = ('Client',  'IterClient', 'SoapFaultError', 'islst')

# global config - probably no reason to change them except in tests
gzipRequest = True    # are we going to gzip the request ?
gzipResponse = True   # are we going to tell the server to gzip the response ?
# obsoleted setting - it must be forceHttp=False for the current Salesforce
forceHttp = False     # force all connections to be HTTP, for debugging
