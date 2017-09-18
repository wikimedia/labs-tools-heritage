#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for update_database."""

import unittest

import mock

from erfgoedbot import monument_tables


class TestProcessClassicConfig(unittest.TestCase):

    """Test process_classic_config()."""

    def setUp(self):
        patcher = mock.patch(
            'erfgoedbot.monument_tables.load_classic_template_sql')
        self.load_sql = patcher.start()
        self.load_sql.return_value = '{table}|{primkey}|  {rows}'
        self.addCleanup(patcher.stop)
        patcher = mock.patch(
            'erfgoedbot.monument_tables.validate_primkey')
        self.validate_primkey = patcher.start()
        self.validate_primkey.return_value = 'primkey'
        self.addCleanup(patcher.stop)
        self.country_config = {
            "table": "the_table",
            "primkey": "the_primkey",
            "fields": []
        }

    def test_process_classic_config_no_fields(self):
        self.fields = []
        expected_output = ("the_table|primkey|  ")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_simple_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_unicode_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": u"s_val_öé"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_multiple_fields(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val"})
        self.country_config["fields"].append(
            {"dest": "d_val_2", "source": "s_val_2"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '',\n"
                           "  `d_val_2` varchar(255) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_nodest_field(self):
        self.country_config["fields"].append(
            {"dest": "", "source": "s_val"})
        expected_output = ("the_table|primkey|  ")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_lat_field(self):
        self.country_config["fields"].append(
            {"dest": "lat", "source": "lat"})
        expected_output = ("the_table|primkey|"
                           "  `lat` double DEFAULT NULL,")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_lon_field(self):
        self.country_config["fields"].append(
            {"dest": "lon", "source": "lon"})
        expected_output = ("the_table|primkey|"
                           "  `lon` double DEFAULT NULL,")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_conv_field(self):
        """Test that conv does not affect output."""
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val",
             "conv": "generateRegistrantUrl"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_check_field(self):
        """Test that check does not affect output."""
        self.country_config["fields"].append(
            {"dest": "lon", "source": "lon", "check": "checkLat"})
        expected_output = ("the_table|primkey|"
                           "  `lon` double DEFAULT NULL,")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_notype_field(self):
        """Ensure empty type is treated as varchar(255)."""
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": ""})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_default_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "default": "0"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '0',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_varchar_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "varchar(14)"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(14) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_int_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "int(11)"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` int(11) NOT NULL DEFAULT 0,")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_autoincrement_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "int(11)",
             "auto_increment": True})
        expected_output = ("the_table|primkey|"
                           "  `d_val` int(11) NOT NULL AUTO_INCREMENT,")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_autoincrement_false_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "int(11)",
             "auto_increment": False})
        expected_output = ("the_table|primkey|"
                           "  `d_val` int(11) NOT NULL DEFAULT 0,")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_other_type_field(self):
        """Ensure unknown types are skipped entirely."""
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "enum('BC','BIC')"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` enum('BC','BIC'),")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)

    def test_process_classic_config_with_primkey(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val"})
        self.country_config["fields"].append(
            {"dest": "d_val_2", "source": "s_val_2"})
        self.country_config["fields"].append(
            {"dest": "d_val_3", "source": "s_val_3"})
        expected_output = ("the_table|primkey|"
                           "  `d_val` varchar(255) NOT NULL DEFAULT '',\n"
                           "  `d_val_2` varchar(255) NOT NULL DEFAULT '',\n"
                           "  `d_val_3` varchar(255) NOT NULL DEFAULT '',")
        result = monument_tables.process_classic_config(self.country_config)
        self.assertEqual(result, expected_output)
