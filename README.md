# Beatbox [![Build Status](https://travis-ci.org/superfell/Beatbox.svg?branch=master)](https://travis-ci.org/superfell/Beatbox)

is a minimal dependency python library for accessing the salesforce.com web services API.

Its primary dependency is on xmltramp, an xml parser library that exposes access to the xml document in an easy to use manner.

Beatbox is released under the GPL v2.

[http://www.pocketsoap.com/beatbox/](http://www.pocketsoap.com/beatbox/)

Beatbox requires Python 2.7.9 or later or Python 3.4 or later. Thanks [hynekcer](https://github.com/hynekcer) for the Python 3 support!

## Installation (Python 3)

The beatbox3 PyPI is stale and not Python 3 compatible (refer to issue #46). 

To ensure that you are using the latest python3 compatible version please install using pip syntax:

#### Command line:
`pip install -e git+https://github.com/superfell/Beatbox@master#egg=beatbox`

#### In requirements.txt:
`-e git+https://github.com/superfell/Beatbox@master#egg=beatbox`

## About TLS 1.2 Support

During 2016 Salesforce plans to [disable TLS 1.0](https://help.salesforce.com/apex/HTViewSolution?id=000221207) support on their service. 
In order for Beatbox to continue working you need to use
a python environment that supports TLS 1.2, to do that you need to use Python 2.7.9 (or any newer 2.x version) and your OpenSSL version
needs to be 1.0.1 or greater. You can run `python --version` to check your python version and `python -c "import ssl; print ssl.OPENSSL_VERSION"` to check the version of OpenSSL that python is using.

Note that if you're on OSX, its bundled with an older version of openSSL than is required. 
If you see an error similar to `ssl.SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure`  or 
`UNSUPPORTED_CLIENT: TLS 1.0 has been disabled in this organization. Please use TLS 1.1 or higher when connecting to Salesforce using https.` you need to update your python and/or OpenSSL versions.

## About PyPi/Beatbox

This version of Beatbox is not fully compatibile with the version at https://pypi.python.org/pypi/beatbox/32.1 See [issue #43](https://github.com/superfell/Beatbox/issues/43) for all the details.
