import unittest
import beatbox

class TestXmlWriter(unittest.TestCase):

    def test_endElement(self):
        w = beatbox.XmlWriter(False)
        w.startPrefixMapping("q", "urn:test")
        w.startElement("urn:test", "root")
        w.startElement("urn:test", "child")
        w.characters("text")
        w.endElement()
        w.endElement()
        xml = w.endDocument()
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:child>text</q:child></q:root>", xml)

    def test_writeStringElement(self):
        w = beatbox.XmlWriter(False)
        w.startPrefixMapping("q", "urn:test")
        w.startElement("urn:test", "root")
        w.writeStringElement("urn:test", "child", ["a","b"])
        w.endElement()
        xml = w.endDocument()
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:test\"><q:child>a</q:child><q:child>b</q:child></q:root>", xml)

if __name__ == '__main__':
    unittest.main()
