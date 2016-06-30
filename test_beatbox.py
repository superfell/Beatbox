import unittest
import beatbox
import datetime
import gzip
from beatbox_six import BytesIO

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
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:child>text</q:child></q:root>", xml)

    def test_writeStringElementList(self):
        self.w.writeStringElement("urn:test", "child", ["a","b"])
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:child>a</q:child><q:child>b</q:child></q:root>", xml)

    def test_writeStringElementOne(self):
        self.w.writeStringElement("urn:test", "child", "a")
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:child>a</q:child></q:root>", xml)

    def test_characterTypes(self):
        self.w.writeStringElement("urn:test", "float", 42.42)
        self.w.writeStringElement("urn:test", "int", 4242)
        self.w.writeStringElement("urn:test", "date", datetime.date(2016,6,30))
        self.w.writeStringElement("urn:test", "dt", datetime.datetime(2016,6,30,21,22,23))
        self.w.endElement()
        xml = self.w.endDocument()
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:float>42.42</q:float>" +
            b"<q:int>4242</q:int>" +
            b"<q:date>2016-06-30</q:date>" +
            b"<q:dt>2016-06-30T21:22:23</q:dt>" +
            b"</q:root>", xml)

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
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:child>text</q:child></q:root>", xml)

if __name__ == '__main__':
    unittest.main()
