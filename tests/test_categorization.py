"""Unit tests for categorize_images."""

# from pywikibot.site import APISite
# from pywikibot.exceptions import NoPage
import unittest
import mock
from erfgoedbot import categorize_images


class TestLoadWikipediaCommonscatTemplates(unittest.TestCase):

    """Test the _load_wikipedia_commonscat_templates method."""

    def test_load_wikipedia_commonscat_templates(self):
        """Ensure commonscat json file is present and contains _default key."""
        try:
            data = categorize_images._load_wikipedia_commonscat_templates()
        except IOError:
            self.fail("Commonscat json file not found")
        self.assertIn(u'_default', data.keys())


class TestGetCommonsCatTemplates(unittest.TestCase):

    """Test the getCommonscatTemplates method."""

    def setUp(self):
        patcher = mock.patch('erfgoedbot.categorize_images._load_wikipedia_commonscat_templates')
        self.mock_load_templates = patcher.start()
        self.mock_load_templates.return_value = {
            "_default": [
                "default_template", []
            ],
            "lang_1": [
                "lang_1_main_template", ["lang_1_template_1"]
            ],
            "lang_2": [
                "lang_2_main_template", ["lang_2_template_1", "lang_2_template_2"]
            ],
        }
        self.addCleanup(patcher.stop)

    def test_getCommonscatTemplates_with_defaults(self):
        result = categorize_images.getCommonscatTemplates()
        self.assertEquals(result, [u'default_template'])

    def test_getCommonscatTemplates_with_one_alternative(self):
        result = categorize_images.getCommonscatTemplates(lang='lang_1')
        self.assertEquals(result, [u'lang_1_main_template', u'lang_1_template_1'])

    def test_getCommonscatTemplates_with_two_alternatives(self):
        result = categorize_images.getCommonscatTemplates(lang='lang_2')
        self.assertEquals(
            result, [u'lang_2_main_template', u'lang_2_template_1', u'lang_2_template_2'])

    def test_getCommonscatTemplates_with_wikivoyage(self):
        result = categorize_images.getCommonscatTemplates(project='wikivoyage')
        self.assertEquals(result, [u'default_template'])


class TestReplaceCategories(unittest.TestCase):

    """Test the replace_default_cat_with_new_categories_in_image_text method."""

    def setUp(self):
        self.mock_old_category = mock.Mock()
        self.mock_old_category.title.return_value = "A"
        self.mock_old_category.__str__ = mock.Mock()
        self.mock_old_category.__str__.return_value = 'A'

    def test_replace_categories_with_no_category_present_should_add_new_category(self):
        old_text = ""
        new_categories = ["B"]
        new_text = categorize_images.replace_default_cat_with_new_categories_in_image_text(
            old_text, self.mock_old_category, new_categories)
        expected_text = u'[[Category:B]]'
        self.assertEquals(new_text, expected_text)

    def test_replace_categories_with_main_category_present_and_new_category_should_remove_old_category(self):
        old_text = """
        [[Category:A]]
        """
        new_categories = ["B"]
        new_text = categorize_images.replace_default_cat_with_new_categories_in_image_text(
            old_text, self.mock_old_category, new_categories)
        expected_text = u'[[Category:B]]'
        self.assertEquals(new_text, expected_text)

    def test_replace_categories_with_no_categories_to_add_raise_Exception(self):
        old_text = ""
        new_categories = []
        with self.assertRaises(categorize_images.NoCategoryToAddException):
            categorize_images.replace_default_cat_with_new_categories_in_image_text(
                old_text, self.mock_old_category, new_categories)


class TestFilterOutCategoriesToAdd(unittest.TestCase):

    def setUp(self):
        self.cat_A = self.make_mock_cat('A')
        self.cat_B = self.make_mock_cat('B')
        self.cat_C = self.make_mock_cat('C')
        self.cat_D = self.make_mock_cat('D')
        self.cat_E = self.make_mock_cat('E')
        self.cat_hidden = self.make_mock_cat('F', hidden=True)

    def make_mock_cat(self, title, hidden=False):
        mock_category = mock.create_autospec(
            categorize_images.pywikibot.Category)
        mock_category._link = categorize_images.pywikibot.Link(title, None)
        if hidden:
            mock_category.isHiddenCategory.return_value = True
        else:
            mock_category.isHiddenCategory.return_value = False
        return mock_category

    def test_filter_categories_no_categories(self):
        new_categories = []
        current_categories = []
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertEquals(result, [])

    def test_filter_categories_all_present(self):
        new_categories = [self.cat_A, self.cat_B]
        current_categories = [self.cat_A, self.cat_B, self.cat_C]
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertEquals(result, [])

    def test_filter_out_some_categories_present(self):
        new_categories = [self.cat_A, self.cat_B, self.cat_C]
        current_categories = [self.cat_A, self.cat_B]
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertEquals(result, [self.cat_C])

    def test_filter_out_with_no_categories_among_present(self):
        new_categories = [self.cat_A, self.cat_B, self.cat_C]
        current_categories = [self.cat_D, self.cat_E]
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertItemsEqual(result, [self.cat_A, self.cat_B, self.cat_C])

    def test_filter_out_with_no_categories_present(self):
        new_categories = [self.cat_A, self.cat_B, self.cat_C]
        current_categories = []
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertItemsEqual(result, [self.cat_A, self.cat_B, self.cat_C])

    def test_filter_out_deduplicate_categories(self):
        new_categories = [self.cat_A, self.cat_B, self.cat_A]
        current_categories = []
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertItemsEqual(result, [self.cat_A, self.cat_B])

    def test_filter_out_hidden_categories(self):
        new_categories = [self.cat_A, self.cat_hidden, self.cat_C]
        current_categories = []
        result = categorize_images.filter_out_categories_to_add(
            new_categories, current_categories)
        self.assertItemsEqual(result, [self.cat_A, self.cat_C])


class TestGetCommonsCategoryViaWikidata(unittest.TestCase):

    """Tests the get_Commons_category_via_Wikidata method."""

    def setUp(self):
        self.mock_page = mock.create_autospec(
            categorize_images.pywikibot.Page)
        self.mock_data_item = mock.create_autospec(
            categorize_images.pywikibot.ItemPage)
        self.mock_claim = mock.create_autospec(
            categorize_images.pywikibot.Claim)

        self.mock_claim.getTarget.return_value = u'A category'
        self.mock_data_item.get.return_value = {
            u'claims': {},
            u'sitelinks': {},
        }
        self.claims = {u'P373': [self.mock_claim, ]}
        self.page_sitelink = u'Some page'
        self.category_sitelink = u'Category:Some category'

    # def test_get_Commons_category_via_Wikidata_no_data_item(self):
    #    self.mock_page.data_item.side_effect = NoPage
    #    with self.assertRaises(categorize_images.NoCommonsCatFromWikidataItemException):
    #        categorize_images.get_Commons_category_via_Wikidata(self.mock_page)

    # def test_get_Commons_category_via_Wikidata_no_claim_or_sitelink(self):
    #    expected_site = APISite("commons", "commons")
    #    self.mock_page.data_item.return_value = self.mock_data_item
    #    self.mock_data_item.getSitelink.side_effect = NoPage
    #    with self.assertRaises(categorize_images.NoCommonsCatFromWikidataItemException):
    #        categorize_images.get_Commons_category_via_Wikidata(self.mock_page)
    #        self.mock_data_item.getSitelink.assert_called_once_with(
    #            expected_site)

    def test_get_Commons_category_via_Wikidata_with_claim(self):
        self.mock_page.data_item.return_value = self.mock_data_item
        self.mock_data_item.get.return_value[u'claims'] = self.claims
        expected = u'Category:A category'
        self.assertEquals(
            categorize_images.get_Commons_category_via_Wikidata(self.mock_page),
            expected)

    def test_get_Commons_category_via_Wikidata_with_page_sitelink(self):
        self.mock_page.data_item.return_value = self.mock_data_item
        self.mock_data_item.getSitelink.return_value = self.page_sitelink
        with self.assertRaises(categorize_images.NoCommonsCatFromWikidataItemException):
            categorize_images.get_Commons_category_via_Wikidata(self.mock_page)

    def test_get_Commons_category_via_Wikidata_with_category_sitelink(self):
        self.mock_page.data_item.return_value = self.mock_data_item
        self.mock_data_item.getSitelink.return_value = self.category_sitelink
        expected = u'Category:Some category'
        self.assertEquals(
            categorize_images.get_Commons_category_via_Wikidata(self.mock_page),
            expected)

    def test_get_Commons_category_via_Wikidata_with_claim_and_category_sitelink(self):
        """Ensure claim value is chosen over sitelink value."""
        self.mock_page.data_item.return_value = self.mock_data_item
        self.mock_data_item.get.return_value[u'claims'] = self.claims
        self.mock_data_item.getSitelink.return_value = self.category_sitelink
        expected = u'Category:A category'
        self.assertEquals(
            categorize_images.get_Commons_category_via_Wikidata(self.mock_page),
            expected)


class TestGetCategoriesFromUpperCategories(unittest.TestCase):

    """Test the get_categories_from_upper_categories method."""

    def setUp(self):
        self.mock_page = mock.create_autospec(
            categorize_images.pywikibot.Page)

    def test_get_categories_from_upper_categories_with_no_categories_returns_empty_set(self):
        self.mock_page.categories.return_value = []
        result = categorize_images.get_categories_from_upper_categories(self.mock_page, None)
        self.assertEquals(result, set())
