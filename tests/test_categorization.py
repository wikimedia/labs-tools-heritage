
import unittest
from mock import Mock
from erfgoedbot.categorize_images import \
    replace_default_cat_with_new_categories_in_image_text, \
    filter_out_categories_to_add, \
    remove_base_category_from_categories_to_add_if_present, \
    deduplicate_categories, \
    NoCategoryToAddException


class TestReplaceCategories(unittest.TestCase):

    """Test the replace_default_cat_with_new_categories_in_image_text method."""

    def setUp(self):
        self.mock_old_category = Mock()
        self.mock_old_category.title.return_value = "A"
        self.mock_old_category.__str__ = Mock()
        self.mock_old_category.__str__.return_value = 'A'

    def test_replace_categories_with_no_category_present_should_add_new_category(self):
        old_text = ""
        new_categories = ["B"]
        new_text = replace_default_cat_with_new_categories_in_image_text(old_text, self.mock_old_category, new_categories)
        expected_text = u'[[Category:B]]'
        self.assertEquals(new_text, expected_text)

    def test_replace_categories_with_main_category_present_and_new_category_should_remove_old_category(self):
        old_text = """
        [[Category:A]]
        """
        new_categories = ["B"]
        new_text = replace_default_cat_with_new_categories_in_image_text(old_text, self.mock_old_category, new_categories)
        expected_text = u'[[Category:B]]'
        self.assertEquals(new_text, expected_text)

    def test_replace_categories_with_no_categories_to_add_raise_Exception(self):
        old_text = ""
        new_categories = []
        with self.assertRaises(NoCategoryToAddException):
            new_text = replace_default_cat_with_new_categories_in_image_text(old_text, self.mock_old_category, new_categories)


class TestDeduplicateCategories(unittest.TestCase):

    def test_deduplicate_categories(self):
        new_categories = ['A', 'B', 'A']
        result = deduplicate_categories(new_categories)
        expected = ['A', 'B']
        self.assertItemsEqual(result, expected)

    def test_deduplicate_categories_nothing_to_deduplicate(self):
        new_categories = ['A', 'B']
        result = deduplicate_categories(new_categories)
        expected = ['A', 'B']
        self.assertItemsEqual(result, expected)

    def test_deduplicate_categories_no_categories(self):
        new_categories = []
        result = deduplicate_categories(new_categories)
        expected = []
        self.assertItemsEqual(result, expected)


class TestRemoveBaseCategory(unittest.TestCase):

    def test_remove_category_with_category_present(self):
        result = remove_base_category_from_categories_to_add_if_present(['A', 'B'], 'A')
        self.assertItemsEqual(result, ['B'])

    def test_remove_category_without_category_present(self):
        result = remove_base_category_from_categories_to_add_if_present(['B', 'C'], 'A')
        self.assertItemsEqual(result, ['B', 'C'])


class TestFilterOutCategoriesToAdd(unittest.TestCase):

    def test_filter_categories_all_present(self):
        new_categories = ['A', 'B']
        current_categories = ['A', 'B', 'C']
        result = filter_out_categories_to_add(new_categories, current_categories)
        self.assertEquals(result, [])

    def test_filter_out_some_categories_present(self):
        new_categories = ['A', 'B', 'C']
        current_categories = ['A', 'B']
        result = filter_out_categories_to_add(new_categories, current_categories)
        self.assertEquals(result, ['C'])

    def test_filter_out_with_no_categories_among_present(self):
        new_categories = ['A', 'B', 'C']
        current_categories = ['D', 'E']
        result = filter_out_categories_to_add(new_categories, current_categories)
        self.assertItemsEqual(result, ['A', 'B', 'C'])

    def test_filter_out_with_no_categories_present(self):
        new_categories = ['A', 'B', 'C']
        current_categories = []
        result = filter_out_categories_to_add(new_categories, current_categories)
        self.assertItemsEqual(result, ['A', 'B', 'C'])
