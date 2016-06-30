import unittest
import beatbox

class TestXmlWriter(unittest.TestCase):

    def test_endElement(self):
        w = beatbox.XmlWriter(False)
        w.startPrefixMapping("q", "urn:foo")
        w.startElement("urn:foo", "root")
        w.startElement("urn:foo", "child")
        w.characters("text")
        w.endElement()
        w.endElement()
        xml = w.endDocument()
        self.assertEqual(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<q:root xmlns:q=\"urn:foo\"><q:child>text</q:child></q:root>", xml)

if __name__ == '__main__':
    unittest.main()
