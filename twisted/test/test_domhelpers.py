# -*- test-case-name: twisted.test.test_domhelpers -*-
#
# Twisted, the Framework of Your Internet
# Copyright (C) 2001-2002 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 

"""Specific tests for (some of) the methods in t.web.domhelpers"""

from twisted.trial.unittest import TestCase

from twisted.web import microdom

from twisted.web import domhelpers

class DomHelpersTest(TestCase):
    def test_getElementsByTagName(self):
        doc1=microdom.parseString('<foo/>')
        actual=domhelpers.getElementsByTagName(doc1, 'foo')[0].nodeName
        expected='foo'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        doc2_xml='<a><foo in="a"/><b><foo in="b"/></b><c><foo in="c"/></c><foo in="d"/><foo in="ef"/><g><foo in="g"/><h><foo in="h"/></h></g></a>'
        doc2=microdom.parseString(doc2_xml)
        tag_list=domhelpers.getElementsByTagName(doc2, 'foo')
        actual=''.join([node.getAttribute('in') for node in tag_list])
        expected='abcdefgh'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        doc3_xml='''
<a><foo in="a"/>
    <b><foo in="b"/>
        <d><foo in="d"/>
            <g><foo in="g"/></g>
            <h><foo in="h"/></h>
        </d>
        <e><foo in="e"/>
            <i><foo in="i"/></i>
        </e>
    </b>
    <c><foo in="c"/>
        <f><foo in="f"/>
            <j><foo in="j"/></j>
        </f>
    </c>
</a>'''
        doc3=microdom.parseString(doc3_xml)
        tag_list=domhelpers.getElementsByTagName(doc3, 'foo')
        actual=''.join([node.getAttribute('in') for node in tag_list])
        expected='abdgheicfj'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_gatherTextNodes(self):
        doc1=microdom.parseString('<a>foo</a>')
        actual=domhelpers.gatherTextNodes(doc1)
        expected='foo'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        doc2_xml='<a>a<b>b</b><c>c</c>def<g>g<h>h</h></g></a>'
        doc2=microdom.parseString(doc2_xml)
        actual=domhelpers.gatherTextNodes(doc2)
        expected='abcdefgh'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        doc3_xml='''<a>a<b>b<d>d<g>g</g><h>h</h></d><e>e<i>i</i></e></b><c>c<f>f<j>j</j></f></c></a>'''
        doc3=microdom.parseString(doc3_xml)
        actual=domhelpers.gatherTextNodes(doc3)
        expected='abdgheicfj'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_clearNode(self):
        doc1=microdom.parseString('<a><b><c><d/></c></b></a>')
        a_node=doc1.documentElement
        domhelpers.clearNode(a_node)
        actual=doc1.documentElement.toxml()
        expected='<a></a>'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)
 
        doc2=microdom.parseString('<a><b><c><d/></c></b></a>')
        b_node=doc2.documentElement.childNodes[0]
        domhelpers.clearNode(b_node)
        actual=doc2.documentElement.toxml()
        expected='<a><b /></a>'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        doc3=microdom.parseString('<a><b><c><d/></c></b></a>')
        c_node=doc3.documentElement.childNodes[0].childNodes[0]
        domhelpers.clearNode(c_node)
        actual=doc3.documentElement.toxml()
        expected='<a><b><c /></b></a>'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_get(self):
        doc1=microdom.parseString('<a><b id="bar"/><c class="foo"/></a>')
        node=domhelpers.get(doc1, "foo")
        actual=node.toxml()
        expected='<c class="foo" />'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        node=domhelpers.get(doc1, "bar")
        actual=node.toxml()
        expected='<b id="bar" />'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        self.assertRaises(domhelpers.NodeLookupError, 
                          domhelpers.get, 
                          doc1, 
                          "pzork")

    def test_getIfExists(self):
        doc1=microdom.parseString('<a><b id="bar"/><c class="foo"/></a>')
        node=domhelpers.getIfExists(doc1, "foo")
        actual=node.toxml()
        expected='<c class="foo" />'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        node=domhelpers.getIfExists(doc1, "pzork")
        assert node==None, 'expected None, didn\'t get None'

    def test_getAndClear(self):
        doc1=microdom.parseString('<a><b id="foo"><c></c></b></a>')
        node=domhelpers.getAndClear(doc1, "foo")
        actual=node.toxml()
        expected='<b id="foo" />'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_locateNodes(self):
        doc1=microdom.parseString('<a><b foo="olive"><c foo="olive"/></b><d foo="poopy"/></a>')
        node_list=domhelpers.locateNodes(doc1.childNodes, 'foo', 'olive',
                                         noNesting=1)
        actual=''.join([node.toxml() for node in node_list])
        expected='<b foo="olive"><c foo="olive" /></b>'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        node_list=domhelpers.locateNodes(doc1.childNodes, 'foo', 'olive',
                                         noNesting=0)
        actual=''.join([node.toxml() for node in node_list])
        expected='<b foo="olive"><c foo="olive" /></b><c foo="olive" />'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_getParents(self):
        doc1=microdom.parseString('<a><b><c><d/></c><e/></b><f/></a>')
        node_list=domhelpers.getParents(doc1.childNodes[0].childNodes[0].childNodes[0])
        actual=''.join([node.tagName for node in node_list if hasattr(node, 'tagName')])
        expected='cba'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_findElementsWithAttribute(self):
        doc1=microdom.parseString('<a foo="1"><b foo="2"/><c foo="1"/><d/></a>')
        node_list=domhelpers.findElementsWithAttribute(doc1, 'foo')
        actual=''.join([node.tagName for node in node_list])
        expected='abc'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

        node_list=domhelpers.findElementsWithAttribute(doc1, 'foo', '1')
        actual=''.join([node.tagName for node in node_list])
        expected='ac'
        assert actual==expected, 'expected %s, got %s' % (expected, actual)

    def test_findNodesNamed(self):
        doc1=microdom.parseString('<doc><foo/><bar/><foo>a</foo></doc>')
        node_list=domhelpers.findNodesNamed(doc1, 'foo')
        actual=len(node_list)
        expected=2
        assert actual==expected, 'expected %d, got %d' % (expected, actual)

    # NOT SURE WHAT THESE ARE SUPPOSED TO DO..
    # def test_RawText  FIXME
    # def test_superSetAttribute FIXME
    # def test_superPrependAttribute FIXME
    # def test_superAppendAttribute FIXME
    # def test_substitute FIXME
