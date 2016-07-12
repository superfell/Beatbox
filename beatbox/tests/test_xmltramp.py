import unittest
from beatbox.xmltramp import Element, Namespace, parse, quote


class XmlTrampTests(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(parse("<doc />")), "")
        self.assertEqual(str(parse("<doc>I <b>love</b> you.</doc>")), "I love you.")
        self.assertEqual(parse("<doc>\nmom\nwow\n</doc>")[0].strip(), "mom\nwow")
        self.assertEqual(str(parse('<bing>  <bang> <bong>center</bong> </bang>  </bing>')), "center")
        self.assertEqual(str(parse('<doc>\xcf\x80</doc>')), '\xcf\x80')

    def test_attr(self):
        d = Element('foo',
                    attrs={'foo': 'bar'},
                    children=['hit with a', Element('bar'), Element('bar')])

        try:
            d._doesnotexist
            raise RuntimeError("Expected Error but found success. Damn.")
        except AttributeError:
            pass
        self.assertEqual(d.bar._name, 'bar')
        try:
            d.doesnotexist
            raise RuntimeError("Expected Error but found success. Damn.")
        except AttributeError:
            pass

        self.assertTrue(hasattr(d, 'bar'))

        self.assertEqual(d('foo'), 'bar')
        d(silly='yes')
        self.assertEqual(d('silly'), 'yes')
        self.assertEqual(d(), d._attrs)

        self.assertEqual(d[0], 'hit with a')
        d[0] = 'ice cream'
        self.assertEqual(d[0], 'ice cream')
        del d[0]
        self.assertEqual(d[0]._name, "bar")
        self.assertEqual(len(d[:]), len(d._dir))
        self.assertEqual(len(d[1:]), len(d._dir) - 1)
        self.assertEqual(len(d['bar':]), 2)
        d['bar':] = 'baz'
        self.assertEqual(len(d['bar':]), 3)
        self.assertEqual(d['bar']._name, 'bar')

    def test_ns(self):
        d = Element('foo')

        doc = Namespace("http://example.org/bar")
        bbc = Namespace("http://example.org/bbc")
        dc = Namespace("http://purl.org/dc/elements/1.1/")
        d = parse("""
        <doc version="2.7182818284590451"
          xmlns="http://example.org/bar"
          xmlns:dc="http://purl.org/dc/elements/1.1/"
          xmlns:bbc="http://example.org/bbc">
            <author>John Polk and John Palfrey</author>
            <dc:creator>John Polk</dc:creator>
            <dc:creator>John Palfrey</dc:creator>
            <bbc:show bbc:station="4">Buffy</bbc:show>
        </doc>""")

        self.assertEqual(repr(d), '<doc version="2.7182818284590451">...</doc>')
        # the order of xmlns attributes is not garanteed invariant
        self.assertEqual(
                d.__repr__(1),
                '<doc xmlns="http://example.org/bar" xmlns:bbc="http://example.org/bbc"'
                ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
                ' version="2.7182818284590451">'
                '<author>John Polk and John Palfrey</author>'
                '<dc:creator>John Polk</dc:creator>'
                '<dc:creator>John Palfrey</dc:creator>'
                '<bbc:show bbc:station="4">Buffy</bbc:show>'
                '</doc>'
                )
        self.assertEqual(
                d.__repr__(1, 1),
                '<doc xmlns="http://example.org/bar"'
                ' xmlns:bbc="http://example.org/bbc" xmlns:dc="http://purl.org/dc/elements/1.1/"'
                ' version="2.7182818284590451">\n'
                '\t<author>John Polk and John Palfrey</author>\n'
                '\t<dc:creator>John Polk</dc:creator>\n'
                '\t<dc:creator>John Palfrey</dc:creator>\n'
                '\t<bbc:show bbc:station="4">Buffy</bbc:show>\n'
                '</doc>',
                )

        self.assertEqual(
                parse('<doc>a<baz>f<b>o</b>ob<b>a</b>r</baz>a</doc>').__repr__(1, 1),
                '<doc>\n'
                '\ta\n'
                '\t<baz>\n'
                '\t\tf\n'
                '\t\t<b>o</b>\n'
                '\t\tob\n'
                '\t\t<b>a</b>\n'
                '\t\tr\n'
                '\t</baz>\n'
                '\ta\n'
                '</doc>')

        self.assertEqual(repr(parse("<doc xml:lang='en' />")), '<doc xml:lang="en"></doc>')

        self.assertEqual(str(d.author), str(d['author']))
        self.assertEqual(str(d.author), "John Polk and John Palfrey")
        self.assertEqual(d.author._name, doc.author)
        self.assertEqual(str(d[dc.creator]), "John Polk")
        self.assertEqual(d[dc.creator]._name, dc.creator)
        self.assertEqual(str(d[dc.creator:][1]), "John Palfrey")
        d[dc.creator] = "Me!!!"
        self.assertEqual(str(d[dc.creator]), "Me!!!")
        self.assertEqual(len(d[dc.creator:]), 1)
        d[dc.creator:] = "You!!!"
        self.assertEqual(len(d[dc.creator:]), 2)

        self.assertEqual(d[bbc.show](bbc.station), "4")
        d[bbc.show](bbc.station, "5")
        self.assertEqual(d[bbc.show](bbc.station), "5")

    def test_text(self):
        e = Element('e')
        e.c = '<img src="foo">'
        self.assertEqual(e.__repr__(1), '<e><c>&lt;img src="foo"></c></e>')
        e.c = '2 > 4'
        self.assertEqual(e.__repr__(1), '<e><c>2 > 4</c></e>')
        e.c = 'CDATA sections are <em>closed</em> with ]]>.'
        self.assertEqual(e.__repr__(1), '<e><c>CDATA sections are &lt;em>closed&lt;/em> with ]]&gt;.</c></e>')
        e.c = parse('<div xmlns="http://www.w3.org/1999/xhtml">i<br /><span></span>love<br />you</div>')
        self.assertEqual(e.__repr__(1), (
                '<e><c><div xmlns="http://www.w3.org/1999/xhtml">i<br /><span></span>love<br />you'
                '</div></c></e>'))

        e = Element('e')
        e('c', 'that "sucks"')
        self.assertEqual(e.__repr__(1), '<e c="that &quot;sucks&quot;"></e>')

        self.assertEqual(quote("]]>"), "]]&gt;")
        self.assertEqual(quote('< dkdkdsd dkd sksdksdfsd fsdfdsf]]> kfdfkg >'),
                         '&lt; dkdkdsd dkd sksdksdfsd fsdfdsf]]&gt; kfdfkg >')

        self.assertEqual(parse('<x a="&lt;"></x>').__repr__(1), '<x a="&lt;"></x>')
        self.assertEqual(parse('<a xmlns="http://a"><b xmlns="http://b"/></a>').__repr__(1),
                         '<a xmlns="http://a"><b xmlns="http://b"></b></a>')


if __name__ == '__main__':
    unittest.main()
