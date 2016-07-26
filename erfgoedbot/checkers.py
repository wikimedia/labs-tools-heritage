#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Checker methods"""

import pywikibot

_logger = "update_database"


def reportDataError(errorMsg, wikiPage, exceptWord, comment=''):
    """Report data error to the talk page of the list."""
    if not comment:
        comment = errorMsg

    pywikibot.debug(errorMsg, _logger)
    talkPage = wikiPage.toggleTalkPage()
    try:
        content = talkPage.get()
    except (pywikibot.NoPage, pywikibot.IsRedirectPage):
        content = u''
    if exceptWord and exceptWord not in content:
        content += "\n\n" + errorMsg + " --~~~~" + "\n\n"
        talkPage.put(content, comment)
        return True

    return False


def is_int(s):
    """Check if a string is a valid int."""
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def checkLat(lat, monumentKey, countryconfig, sourcePage):
    """Check if a latitude has a valid value."""
    if len(lat):
        try:
            lat = float(lat)
        except ValueError:
            errorMsg = u"Invalid latitude value: %s for monument %s" % (
                lat, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        countryBbox = ''
        if (countryconfig.get('countryBbox')):
            countryBbox = countryconfig.get('countryBbox')

        if (lat > 90 or lat < -90):
            errorMsg = u"Latitude for monument %s out of range: %s" % (
                monumentKey, lat)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        elif (countryBbox):
            maxsplit = 3
            (left, bottom, right, top) = countryBbox.split(",", maxsplit)
            bottom = float(bottom)
            top = float(top)
            minLat = min(bottom, top)
            maxLat = max(bottom, top)
            if (lat > maxLat or lat < minLat):
                errorMsg = u"Latitude for monument %s out of country area: %s" % (
                    monumentKey, lat)
                reportDataError(errorMsg, sourcePage, monumentKey)
                return False
            else:
                return True
        else:
            return True


def checkLon(lon, monumentKey, countryconfig, sourcePage):
    """Check if a longitude has a valid value."""
    if len(lon):
        try:
            lon = float(lon)
        except ValueError:
            errorMsg = u"Invalid longitude value: %s for monument %s" % (
                lon, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        countryBbox = ''
        if (countryconfig.get('countryBbox')):
            countryBbox = countryconfig.get('countryBbox')

        if (lon > 180 or lon < -180):
            errorMsg = u"Longitude for monument %s out of range: %s" % (
                monumentKey, lon)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        elif (countryBbox):
            maxsplit = 3
            (left, bottom, right, top) = countryBbox.split(",", maxsplit)
            left = float(left)
            right = float(right)
            minLon = min(left, right)
            maxLon = max(left, right)
            if (lon > maxLon or lon < minLon):
                errorMsg = u"Longitude for monument %s out of country area: %s" % (
                    monumentKey, lon)
                reportDataError(errorMsg, sourcePage, monumentKey)
                return False
            else:
                return True
        else:
            return True


def check_wikidata(wd_item, monumentKey, sourcePage):
    """Check that a value is a potential wikidata entity."""
    if len(wd_item):
        if wd_item.startswith('Q') and is_int(wd_item[1:]):
            return True
        else:
            errorMsg = u"Invalid wikidata value: %s for monument %s" % (
                wd_item, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False


def check_lat_with_lon(fieldnames, monumentKey, sourcePage):
    """Check that lat and lon are always paired."""
    if 'lat' in fieldnames and 'lon' not in fieldnames:
        errorMsg = u"Longitude is not set for monument %s." % (
            monumentKey, )
        reportDataError(errorMsg, sourcePage, monumentKey)
    if 'lon' in fieldnames and 'lat' not in fieldnames:
        errorMsg = u"Latitude is not set for monument %s." % (
            monumentKey, )
        reportDataError(errorMsg, sourcePage, monumentKey)
