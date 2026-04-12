"""Unit tests for add_object_location_monuments."""
import unittest
import unittest.mock as mock

import pywikibot

from erfgoedbot import add_object_location_monuments


class TestPutAfterTemplate(unittest.TestCase):
    """Test the putAfterTemplate function."""
    def setUp(self):
        self.mock_site = mock.create_autospec(pywikibot.Site)

    def test_template_found_inserts_after_closing_braces(self):
        """Text is inserted after the closing braces of the template."""
        oldtext = '{{Information|description=A photo}}\nMore text'
        result = add_object_location_monuments.putAfterTemplate(
            oldtext, 'Information', 'INSERTED', self.mock_site)
        self.assertIn('INSERTED', result)
        self.assertIn('{{Information|description=A photo}}', result)
        # INSERTED should appear after the template, not before
        tpl_end = result.index('}}') + 2
        self.assertIn('INSERTED', result[tpl_end:])

    def test_template_found_with_nested_templates(self):
        """Brace counting handles nested templates correctly."""
        oldtext = (
            '{{Information|description={{en|A photo '
            '{{with|nested}}}}}}\nTrailing')
        result = add_object_location_monuments.putAfterTemplate(
            oldtext, 'Information', 'INSERTED', self.mock_site)
        self.assertIn('INSERTED', result)
        self.assertIn('Trailing', result)
        # Nested content must survive
        self.assertIn('{{en|A photo {{with|nested}}}}', result)

    def test_template_not_found_loose_false_returns_empty(self):
        """Returns empty string when template missing and loose=False."""
        result = add_object_location_monuments.putAfterTemplate(
            'No template here', 'Information', 'INSERTED', self.mock_site, loose=False)
        self.assertEqual(result, '')
