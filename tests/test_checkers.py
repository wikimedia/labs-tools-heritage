# -*- coding: utf-8  -*-
"""Unit tests for checkers.

Those that aren't checked through test_update_database
"""

import unittest

import mock

from erfgoedbot import checkers


class TestIsInt(unittest.TestCase):

    def test_empty_string_fail(self):
        s = ''
        result = checkers.is_int(s)
        self.assertEqual(result, False)

    def test_None_fail(self):
        s = None
        result = checkers.is_int(s)
        self.assertEqual(result, False)

    def test_random_string_fail(self):
        s = 'random_string'
        result = checkers.is_int(s)
        self.assertEqual(result, False)

    def test_float_fail(self):
        s = '123.456'
        result = checkers.is_int(s)
        self.assertEqual(result, False)

    def test_valid_int_succeed(self):
        s = '123'
        result = checkers.is_int(s)
        self.assertEqual(result, True)

    def test_other_script_succeed(self):
        s = u'۱۲۳۴۵۶۷۸۹۰'
        result = checkers.is_int(s)
        self.assertEqual(result, True)


class TestCheckersBase(unittest.TestCase):

    def setUp(self):
        self.country_config = {}
        self.mock_page = mock.create_autospec(
            checkers.pywikibot.Page,
        )
        self.mock_page.title.return_value = "MockPageTitle"
        self.monumentKey = 'Some-key'


class TestCountryBboxRequireLatLon(TestCheckersBase):

    def setUp(self):
        super(TestCountryBboxRequireLatLon, self).setUp()
        self.fieldnames = ['a_field']

    def test_countryBbox_no_lat_or_lon(self):
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            checkers.check_lat_with_lon(self.fieldnames, self.monumentKey, self.mock_page)
            assert not mock_reportDataError.called  # mock 3.5 has assert_not_called()

    def test_countryBbox_lat_no_lon(self):
        self.fieldnames.append('lat')
        expected_errorMsg = u"Longitude is not set for monument %s." % self.monumentKey

        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            checkers.check_lat_with_lon(self.fieldnames, self.monumentKey, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)

    def test_countryBbox_lon_no_lat(self):
        self.fieldnames.append('lon')
        expected_errorMsg = u"Latitude is not set for monument %s." % self.monumentKey

        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            checkers.check_lat_with_lon(self.fieldnames, self.monumentKey, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)

    def test_countryBbox_lat_and_lon(self):
        self.fieldnames += ['lat', 'lon']
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            checkers.check_lat_with_lon(self.fieldnames, self.monumentKey, self.mock_page)
            assert not mock_reportDataError.called  # mock 3.5 has assert_not_called()


class TestCheckLatNoCountryBbox(TestCheckersBase):

    def test_empty_lat(self):
        lat = ''
        result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, None)

    def test_non_float_lat(self):
        lat = 'some_string'
        expected_errorMsg = u"Invalid latitude value: %s for monument %s" % (
            lat, self.monumentKey)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_positive_out_of_bounds_lat(self):
        lat = '90.1'
        expected_errorMsg = u"Latitude for monument %s out of range: %s" % (
            self.monumentKey, lat)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_negative_out_of_bounds_lat(self):
        lat = '-90.1'
        expected_errorMsg = u"Latitude for monument %s out of range: %s" % (
            self.monumentKey, lat)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_valid_int_lat(self):
        lat = '85'
        result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, True)

    def test_valid_float_lat(self):
        lat = '-13.37'
        result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, True)


class TestCheckLatWithCountryBbox(TestCheckersBase):

    def setUp(self):
        super(TestCheckLatWithCountryBbox, self).setUp()
        self.country_config['countryBbox'] = u'8.5,10.5,28.0,60.0'

    def test_lat_outside_Bbox(self):
        lat = '-1.337'
        expected_errorMsg = u"Latitude for monument %s out of country area: %s" % (
            self.monumentKey, lat)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_lat_inside_Bbox(self):
        lat = '13.37'
        result = checkers.checkLat(lat, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, True)


class TestCheckLonNoCountryBbox(TestCheckersBase):

    def test_empty_lon(self):
        lon = ''
        result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, None)

    def test_non_float_lon(self):
        lon = 'some_string'
        expected_errorMsg = u"Invalid longitude value: %s for monument %s" % (
            lon, self.monumentKey)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_positive_out_of_bounds_lon(self):
        lon = '180.1'
        expected_errorMsg = u"Longitude for monument %s out of range: %s" % (
            self.monumentKey, lon)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_negative_out_of_bounds_lon(self):
        lon = '-180.1'
        expected_errorMsg = u"Longitude for monument %s out of range: %s" % (
            self.monumentKey, lon)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_valid_int_lon(self):
        lon = '85'
        result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, True)

    def test_valid_float_lon(self):
        lon = '-13.37'
        result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, True)


class TestCheckLonWithCountryBbox(TestCheckersBase):

    def setUp(self):
        super(TestCheckLonWithCountryBbox, self).setUp()
        self.country_config['countryBbox'] = u'8.5,10.5,28.0,60.0'

    def test_lon_outside_Bbox(self):
        lon = '-1.337'
        expected_errorMsg = u"Longitude for monument %s out of country area: %s" % (
            self.monumentKey, lon)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_lon_inside_Bbox(self):
        lon = '13.37'
        result = checkers.checkLon(lon, self.monumentKey, self.country_config, self.mock_page)
        self.assertEqual(result, True)


class TestCheckWikidata(TestCheckersBase):

    def setUp(self):
        super(TestCheckWikidata, self).setUp()
        self.error_msg = u"Invalid wikidata value: %s for monument %s"

    def test_empty_wd_item(self):
        wd_item = ''
        result = checkers.check_wikidata(wd_item, self.monumentKey, self.mock_page)
        self.assertEqual(result, None)

    def test_non_Q_part(self):
        wd_item = 'P123'
        expected_errorMsg = self.error_msg % (wd_item, self.monumentKey)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.check_wikidata(wd_item, self.monumentKey, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_non_integer_part(self):
        wd_item = 'Que?'
        expected_errorMsg = self.error_msg % (wd_item, self.monumentKey)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.check_wikidata(wd_item, self.monumentKey, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_valid_wd_item(self):
        wd_item = 'Q123'
        result = checkers.check_wikidata(wd_item, self.monumentKey, self.mock_page)
        self.assertEqual(result, True)


class TestCheckInteger(TestCheckersBase):

    def setUp(self):
        super(TestCheckInteger, self).setUp()
        self.error_msg = u"Invalid integer value: %s for monument %s"

    def test_check_integer_empty_string(self):
        text = ''
        expected_errorMsg = self.error_msg % (text, self.monumentKey)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.check_integer(text, self.monumentKey, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_check_integer_random_string(self):
        text = 'random string'
        expected_errorMsg = self.error_msg % (text, self.monumentKey)
        with mock.patch('erfgoedbot.checkers.reportDataError', autospec=True) as mock_reportDataError:
            result = checkers.check_integer(text, self.monumentKey, self.mock_page)
            mock_reportDataError.assert_called_once_with(expected_errorMsg, self.mock_page, self.monumentKey)
            self.assertEqual(result, False)

    def test_check_integer_valid_integer_string(self):
        text = '123'
        result = checkers.check_integer(text, self.monumentKey, self.mock_page)
        self.assertEqual(result, True)

    def test_check_integer_valid_integer_int(self):
        text = 123
        result = checkers.check_integer(text, self.monumentKey, self.mock_page)
        self.assertEqual(result, True)
