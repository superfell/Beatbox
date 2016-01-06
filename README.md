# Beatbox 

is a minimal dependency python library for accessing the salesforce.com web services API.

Its primary dependency is on xmltramp, a xml parser library that exposes access to the xml document in an easy to use manner.

Beatbox is released under the GPL v2.

[http://www.pocketsoap.com/beatbox/](http://www.pocketsoap.com/beatbox/)

## About TLS 1.2 Support

During 2016 Salesforce plans to [disable TLS 1.0](https://help.salesforce.com/apex/HTViewSolution?id=000221207) support on their service. 
In order for Beatbox to continue working you need to use
a python environment that supports TLS 1.2, to do that you need to use Python 2.7.9 (or any newer 2.x version) and your OpenSSL version
needs to be 1.0.1 or greater. You can run `python --version` to check your python version and `openssl version` to check your openSSL
version. Note that if you're on OSX, its bundled with an older version of openSSL than is required. 
If you see an error similar to `ssl.SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure` 
you need to update your python and/or openSSL versions.
