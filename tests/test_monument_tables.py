#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for update_database."""

import unittest
import StringIO

from erfgoedbot import monument_tables


class TestProcessClassicConfig(unittest.TestCase):

    """Test process_classic_config()."""

    def setUp(self):
        self.country_config = {"fields": []}
        self.output = StringIO.StringIO()

    def tearDown(self):
        self.output.close()

    def test_process_classic_config_no_fields(self):
        expected_output = 'extra_cols\n'
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_simple_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val"})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_unicode_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": u"s_val_öé"})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_multiple_fields(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val"})
        self.country_config["fields"].append(
            {"dest": "d_val_2", "source": "s_val_2"})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '',\n" \
                          "  `d_val_2` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_multiple_fields_article(self):
        self.country_config["fields"].append(
            {"dest": "d_val_1", "source": "s_val_2"})
        self.country_config["fields"].append(
            {"dest": "monument_article", "source": "name"})
        self.country_config["fields"].append(
            {"dest": "d_val_2", "source": "s_val_2"})
        expected_output = "  `d_val_1` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n" \
                          "  `monument_article` varchar(255) NOT NULL DEFAULT '',\n" \
                          "  `d_val_2` varchar(255) NOT NULL DEFAULT '',\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_nodest_field(self):
        self.country_config["fields"].append(
            {"dest": "", "source": "s_val"})
        expected_output = "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_lat_field(self):
        self.country_config["fields"].append(
            {"dest": "lat", "source": "lat"})
        expected_output = "  `lat` double DEFAULT NULL,\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_lon_field(self):
        self.country_config["fields"].append(
            {"dest": "lon", "source": "lon"})
        expected_output = "  `lon` double DEFAULT NULL,\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_conv_field(self):
        """Test that conv does not affect output."""
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val",
             "conv": "generateRegistrantUrl"})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_check_field(self):
        """Test that check does not affect output."""
        self.country_config["fields"].append(
            {"dest": "lon", "source": "lon", "check": "checkLat"})
        expected_output = "  `lon` double DEFAULT NULL,\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_notype_field(self):
        """Ensure empty type is treated as varchar(255)."""
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": ""})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_default_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "default": "0"})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '0',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_varchar_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "varchar(14)"})
        expected_output = "  `d_val` varchar(14) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_int_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "int(11)"})
        expected_output = "  `d_val` int(11) NOT NULL DEFAULT 0,\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_autoincrement_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "int(11)",
             "auto_increment": True})
        expected_output = "  `d_val` int(11) NOT NULL AUTO_INCREMENT,\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_autoincrement_false_field(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "int(11)",
             "auto_increment": False})
        expected_output = "  `d_val` int(11) NOT NULL DEFAULT 0,\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_other_type_field(self):
        """Ensure unknown types are skipped entirely."""
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val", "type": "enum('BC','BIC')"})
        expected_output = "  `d_val` enum('BC','BIC'),\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'no_primkey', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertFalse(result)

    def test_process_classic_config_with_primkey(self):
        self.country_config["fields"].append(
            {"dest": "d_val", "source": "s_val"})
        self.country_config["fields"].append(
            {"dest": "d_val_2", "source": "s_val_2"})
        self.country_config["fields"].append(
            {"dest": "d_val_3", "source": "s_val_3"})
        expected_output = "  `d_val` varchar(255) NOT NULL DEFAULT '',\n" \
                          "  `d_val_2` varchar(255) NOT NULL DEFAULT '',\n" \
                          "  `d_val_3` varchar(255) NOT NULL DEFAULT '',\n" \
                          "extra_cols\n"
        result = monument_tables.process_classic_config(
            self.output, self.country_config, 'd_val_2', 'extra_cols\n')
        self.assertEqual(self.output.getvalue(), expected_output)
        self.assertEqual(result, "d_val_2")
