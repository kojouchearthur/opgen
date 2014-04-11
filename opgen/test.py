import unittest
import os
import pprint

from parser import ContentParser, Utils

parser = ContentParser()

class TestParser(unittest.TestCase):
    
    def test_load_files(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        pages = Utils.find_pages(dirpath+'/../pages/')
        assert len(pages) is 4

    def test_parse_attr(self):
        self.assertEqual(parser._parse_attr(' hello="world"', "hello"), "world")
        self.assertEqual(parser._parse_attr(' other="hello" hello="world" ', "hello"), "world")
        self.assertEqual(parser._parse_attr(' other="hello" hello="world war 3" ', "hello"), "world war 3")
        self.assertEqual(parser._parse_attr(' hello=\'worldo\'', "hello"), "worldo")

    def test_parse(self):
        content = parser.parse_content('<page-ref slug="my-slug" label=\'My label\' /> <p>the content...</p>')
        self.assertEqual('My label', content['label'])
        self.assertEqual('my-slug', content['slug'])
        self.assertEqual('<p>the content...</p>', content['content'])

    def test_empty_parse(self):
        content = parser.parse_content('as is')
        assert content['content'] is 'as is'
        assert content['slug'] is ''

    def test_parse_section(self):
        content = parser.parse_content('<p>...</p> <h3 data-page-section="test:value">Testing</h3> <p></p> <h3 data-page-section="test2">Test2</h3>');
        assert len(content['sections']) is 2
        self.assertEqual(content['sections']['test'], 'value')
        self.assertEqual(content['sections']['test2'], 'test2')

if __name__ == '__main__':
    unittest.main()