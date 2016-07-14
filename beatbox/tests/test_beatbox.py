import unittest
import datetime
import gzip

import beatbox
from beatbox import xmltramp
from beatbox.six import BytesIO


class TestXmlWriter(unittest.TestCase):

    def setUp(self):
        self.w = beatbox.XmlWriter(False)
        self.w.startPrefixMapping("q", "urn:test")
        self.w.startElement("urn:test", "root")

    def test_endElement(self):
        self.w.startElement("urn:test", "child")
        self.w.characters("text")
        self.w.endElement()
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b'<?xml version="1.0" encoding="utf-8"?>\n'
                         b'<q:root xmlns:q="urn:test"><q:child>text</q:child></q:root>', xml)

    def test_mixedUnicode(self):
        self.w.startElement(u"urn:test", u"child")
        self.w.characters(u"text A acute \u00c1.")
        self.w.characters(b"text A acute \xc3\x81.")
        self.w.endElement()
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b'<?xml version="1.0" encoding="utf-8"?>\n<q:root xmlns:q="urn:test"><q:child>'
                         b'text A acute \xc3\x81.'
                         b'text A acute \xc3\x81.</q:child></q:root>', xml)

    def test_writeStringElementList(self):
        self.w.writeStringElement("urn:test", "child", ["a", "b"])
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b'<?xml version="1.0" encoding="utf-8"?>\n'
                         b'<q:root xmlns:q="urn:test"><q:child>a</q:child><q:child>b</q:child></q:root>', xml)

    def test_writeStringElementOne(self):
        self.w.writeStringElement("urn:test", "child", "a")
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b'<?xml version="1.0" encoding="utf-8"?>\n'
                         b'<q:root xmlns:q="urn:test"><q:child>a</q:child></q:root>', xml)

    def test_characterTypes(self):
        self.w.writeStringElement("urn:test", "float", 42.42)
        self.w.writeStringElement("urn:test", "int", 4242)
        self.w.writeStringElement("urn:test", "date", datetime.date(2016, 6, 30))
        self.w.writeStringElement("urn:test", "dt", datetime.datetime(2016, 6, 30, 21, 22, 23))
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(
            b'<?xml version="1.0" encoding="utf-8"?>\n<q:root xmlns:q="urn:test"><q:float>42.42</q:float>' +
            b'<q:int>4242</q:int>' +
            b'<q:date>2016-06-30</q:date>' +
            b'<q:dt>2016-06-30T21:22:23</q:dt>' +
            b'</q:root>', xml)

    def test_gzip(self):
        # note this doesn't use self.w as that's not configured to zip
        w = beatbox.XmlWriter(True)
        w.startPrefixMapping("q", "urn:test")
        w.startElement("urn:test", "root")
        w.writeStringElement("urn:test", "child", "text")
        w.endElement()
        zipped = w.endDocument()
        gz = gzip.GzipFile(fileobj=BytesIO(zipped))
        xml = gz.read()
        self.assertEqual(b'<?xml version="1.0" encoding="utf-8"?>\n'
                         b'<q:root xmlns:q="urn:test"><q:child>text</q:child></q:root>', xml)


soapEnvElement = (
    b'<?xml version="1.0" encoding="utf-8"?>\n'
    b'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"'
    b' xmlns:p="urn:partner.soap.sforce.com"'
    b' xmlns:o="urn:sobject.partner.soap.sforce.com"'
    b' xmlns:x="http://www.w3.org/2001/XMLSchema-instance">')


class TestSoapWriter(unittest.TestCase):

    def setUp(self):
        beatbox.gzipRequest = False

    def test_xsiNil(self):
        w = beatbox.SoapWriter()
        w.writeStringElement("http://schemas.xmlsoap.org/soap/envelope/", "Body", None)
        xml = w.endDocument()
        self.assertEqual(soapEnvElement +
                         b'<s:Body x:nil="true"></s:Body>' +
                         b'</s:Envelope>', xml)

    def test_xsiNilWithAtttrs(self):
        w = beatbox.SoapWriter()
        a = {(beatbox._envNs, "mustUnderstand"): "1"}
        w.writeStringElement("http://schemas.xmlsoap.org/soap/envelope/", "Header", None, a)
        xml = w.endDocument()
        # because attributes aren't ordered, we can't do a simple sting assert check here
        # we need to actually parse and verify the xml that way
        root = xmltramp.parse(xml)
        hdr = root[0]
        soapNs = xmltramp.Namespace("http://schemas.xmlsoap.org/soap/envelope/")
        xsiNs = xmltramp.Namespace("http://www.w3.org/2001/XMLSchema-instance")
        self.assertEqual("1", hdr(soapNs.mustUnderstand))
        self.assertEqual("true", hdr(xsiNs.nil))


class TestSoapEnvelope(unittest.TestCase):

    def setUp(self):
        beatbox.gzipRequest = False

    def test_makeEnvelope(self):
        e = beatbox.SoapEnvelope("http://localhost", "bob", "Beatbox/0.96")
        env = e.makeEnvelope()
        self.assertEqual(
            soapEnvElement +
            b'<s:Header>\n' +
            b'<p:CallOptions><p:client>Beatbox/0.96</p:client></p:CallOptions>\n' +
            b'</s:Header><s:Body>\n' +
            b'<p:bob></p:bob>' +
            b'</s:Body></s:Envelope>', env)


def all_tests():
    """Test suite for setup.py that combines all *unit* tests to one suite."""
    loader = unittest.defaultTestLoader
    return unittest.TestSuite([loader.loadTestsFromModule(xmltramp),
                               loader.loadTestsFromTestCase(TestXmlWriter),
                               loader.loadTestsFromTestCase(TestSoapWriter),
                               loader.loadTestsFromTestCase(TestSoapEnvelope)
                               ])


if __name__ == '__main__':
    unittest.main()
