"""Unit tests for categorize_images."""

# from pywikibot.site import APISite
# from pywikibot.exceptions import NoPage
import unittest

import mock

import pywikibot

from erfgoedbot import categorize_images


class TestCreateReportBase(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch(
            'erfgoedbot.categorize_images.common.save_to_wiki_or_local')
        self.mock_save_to_wiki_or_local = patcher.start()
        self.addCleanup(patcher.stop)

        # silence logger
        patcher = mock.patch(
            'erfgoedbot.categorize_images.pywikibot.debug')
        self.mock_debug = patcher.start()
        self.addCleanup(patcher.stop)


class TestLoadWikipediaCommonscatTemplates(unittest.TestCase):

    """Test the _load_wikipedia_commonscat_templates method."""

    def test_load_wikipedia_commonscat_templates(self):
        """Ensure commonscat json file is present and contains _default key."""
        try:
            data = categorize_images._load_wikipedia_commonscat_templates()
        except IOError:
            self.fail("Commonscat json file not found")
        self.assertIn(u'_default', data.keys())


class TestLoadIgnoredCategories(unittest.TestCase):

    """Test the _load_ignored_categories method."""

    def test__load_ignored_categories(self):
        """Ensure ignored categories YAML file is present and decodes to a list."""
        try:
            data = categorize_images._load_ignored_categories()
        except IOError:
            self.fail("YAML file not found")
        self.assertTrue(isinstance(data, list))


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

    def test_filter_out_ignored_categories(self):
        new_categories = [self.cat_A, self.cat_B, self.cat_C]
        current_categories = []
        with mock.patch('erfgoedbot.categorize_images._load_ignored_categories', autospec=True) as mock_load_ignored_categories:
            mock_load_ignored_categories.return_value = [self.cat_B, ]
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


class TestOutputStatistics(TestCreateReportBase):

    """Test the outputStatistics method."""

    def setUp(self):
        super(TestOutputStatistics, self).setUp()

        self.prefix = (
            u'{| class="wikitable sortable"\n'
            u'! country '
            u'! [[:en:List of ISO 639-1 codes|lang]] '
            u'! Base category '
            u'! Template '
            u'! data-sort-type="number"|Total images '
            u'! data-sort-type="number"|Categorized images '
            u'! data-sort-type="number"|Images left '
            u'! data-sort-type="number"|Current image count'
            u'\n')

        self.postfix = (
            u'|- class="sortbottom"\n'
            u'|\n|\n|\n|\n| {0} \n| {1} \n| {2} | \n|}}\n')

        self.comment = (
            u'Updating categorization statistics. '
            u'Total: {0} Categorized: {1} Leftover: {2}')
        commons = pywikibot.Site('commons', 'commons')
        self.page = pywikibot.Page(
            commons, u'Commons:Monuments database/Categorization/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_total_images_sum,
                        expected_categorized_images_sum,
                        expected_leftover_images_sum):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix.format(
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.page,
            self.comment.format(
                expected_total_images_sum,
                expected_categorized_images_sum,
                expected_leftover_images_sum),
            expected_text
        )

    def test_output_statistics_single_complete(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'cat': 'A category',
            'template': 'A template',
            'total_images': 321,
            'cat_images': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| [[:Category:A category]] \n'
            u'| {{tl|A template}} \n'
            u'| 321 \n'
            u'| 123 \n'
            u'| 198 \n'
            u'| {{PAGESINCATEGORY:A category|files}} \n')
        expected_total_images_sum = 321
        expected_categorized_images_sum = 123
        expected_leftover_images_sum = 198

        categorize_images.outputStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)

    def test_output_statistics_basic(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'total_images': 321,
            'cat_images': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| --- \n'
            u'| --- \n'
            u'| 321 \n'
            u'| 123 \n'
            u'| 198 \n'
            u'| --- \n')
        expected_total_images_sum = 321
        expected_categorized_images_sum = 123
        expected_leftover_images_sum = 198

        categorize_images.outputStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)

    def test_output_statistics_basic_skipped(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'cmt': 'skipped: some reason'
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| --- \n'
            u'| --- \n'
            u'| --- \n'
            u'| skipped: some reason \n'
            u'| --- \n'
            u'| --- \n')
        expected_total_images_sum = 0
        expected_categorized_images_sum = 0
        expected_leftover_images_sum = 0

        categorize_images.outputStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)

    def test_output_statistics_basic_no_leftover(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'total_images': 321,
            'cat_images': 321
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| --- \n'
            u'| --- \n'
            u'| 321 \n'
            u'| 321 \n'
            u'| 0 \n'
            u'| --- \n')
        expected_total_images_sum = 321
        expected_categorized_images_sum = 321
        expected_leftover_images_sum = 0

        categorize_images.outputStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)

    def test_output_statistics_multiple_complete(self):
        statistics = [
            {
                'code': 'foo',
                'lang': 'en',
                'total_images': 3,
                'cat_images': 2
            },
            {
                'code': 'bar',
                'lang': 'fr',
                'total_images': 7,
                'cat_images': 3
            }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| --- \n'
            u'| --- \n'
            u'| 3 \n'
            u'| 2 \n'
            u'| 1 \n'
            u'| --- \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| --- \n'
            u'| --- \n'
            u'| 7 \n'
            u'| 3 \n'
            u'| 4 \n'
            u'| --- \n')
        expected_total_images_sum = 10
        expected_categorized_images_sum = 5
        expected_leftover_images_sum = 5

        categorize_images.outputStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)

    def test_output_statistics_multiple_mixed(self):
        statistics = [
            {
                'code': 'foo',
                'lang': 'en',
                'total_images': 3,
                'cat_images': 2
            },
            {
                'code': 'bar',
                'lang': 'fr',
                'cmt': 'oh no!'
            }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| --- \n'
            u'| --- \n'
            u'| 3 \n'
            u'| 2 \n'
            u'| 1 \n'
            u'| --- \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| --- \n'
            u'| --- \n'
            u'| --- \n'
            u'| oh no! \n'
            u'| --- \n'
            u'| --- \n')
        expected_total_images_sum = 3
        expected_categorized_images_sum = 2
        expected_leftover_images_sum = 1

        categorize_images.outputStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_categorized_images_sum,
            expected_leftover_images_sum)
