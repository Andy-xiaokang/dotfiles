import unittest
from .tools import warn
from bottle import MakoTemplate, mako_template, mako_view, touni
import os

views_dir = os.path.join(os.path.dirname(__file__), 'views')

class TestMakoTemplate(unittest.TestCase):
    def test_string(self):
        """ Templates: Mako string"""
        t = MakoTemplate('start ${var} end').render(var='var')
        self.assertEqual('start var end', t)

    def test_file(self):
        """ Templates: Mako file"""
        t = MakoTemplate(name=views_dir + os.sep + 'mako_simple.tpl').render(var='var')
        self.assertEqual('start var end\n', t)

    def test_name(self):
        """ Templates: Mako lookup by name """
        t = MakoTemplate(name='mako_simple', lookup=[views_dir]).render(var='var')
        self.assertEqual('start var end\n', t)

    def test_notfound(self):
        """ Templates: Unavailable templates"""
        self.assertRaises(Exception, MakoTemplate, name="abcdef")

    def test_error(self):
        """ Templates: Exceptions"""
        self.assertRaises(Exception, MakoTemplate, '%for badsyntax')

    def test_inherit(self):
        """ Templates: Mako lookup and inherience """
        t = MakoTemplate(name='mako_inherit', lookup=[views_dir]).render(var='v')
        self.assertEqual('o\ncvc\no\n', t)
        t = MakoTemplate('<%inherit file="mako_base.tpl"/>\nc${var}c\n', lookup=[views_dir]).render(var='v')
        self.assertEqual('o\ncvc\no\n', t)
        t = MakoTemplate('<%inherit file="views/mako_base.tpl"/>\nc${var}c\n', lookup=[os.path.dirname(views_dir)]).render(var='v')
        self.assertEqual('o\ncvc\no\n', t)

    def test_template_shortcut(self):
        result = mako_template('start ${var} end', var='middle')
        self.assertEqual(touni('start middle end'), result)

    def test_view_decorator(self):
        @mako_view('start ${var} end')
        def test():
            return dict(var='middle')
        self.assertEqual(touni('start middle end'), test())


try:
  import mako
except ImportError:
  warn("No Mako template support. Skipping tests.")
  del TestMakoTemplate

if __name__ == '__main__': #pragma: no cover
    unittest.main()

