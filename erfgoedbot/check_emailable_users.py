#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Check whether uploaders are emailable

Usage:
python check_emailable_users.py -delta:120 -category:Images_from_Wiki_Loves_Monuments_2018
"""
import datetime

import pywikibot

from database_connection import (
    close_database_connection,
    connect_to_commons_database
)


def get_users(conn, cursor, category, delta_minutes=120):
    """
    Retrieve the uploaders of images in the given category in the given timeframe.
    (Only registered users, since that’s a requirement to upload to  Wikimedia Commons)
    """
    pywikibot.output("Retrieving users...")
    query = (
        u"SELECT"
        u" user.user_name as uploader"
        u" FROM (SELECT"
        u"   cl_to,"
        u"   cl_from"
        u"   FROM categorylinks"
        u"   WHERE cl_to = %s AND cl_type = 'file') cats"
        u" INNER JOIN page ON cl_from = page_id"
        u" INNER JOIN image ON page_title = img_name"
        u" LEFT JOIN actor ON actor.actor_id = image.img_actor"
        u" LEFT JOIN user ON user.user_id = actor.actor_user"
        u" WHERE img_timestamp BETWEEN %s AND %s"
        u" GROUP BY uploader")

    now = datetime.datetime.utcnow()

    formatter = "%Y%m%d%H%M%S"
    begin_time = (now + datetime.timedelta(minutes=0 - delta_minutes)).strftime(formatter)
    end_time = now.strftime(formatter)

    cursor.execute(query, (category, begin_time, end_time))

    result = cursor.fetchall()
    return result


def notify_user(user):
    talk_page = user.getUserTalkPage()
    try:
        text = "{{subst:WLM-enable-email}}"
        comment = u"Notifying WLM participant of missing e-mail address."
        history_users = [edit[u'user'] for edit in talk_page.getLatestEditors(limit=10)]
        if user.site.username() in history_users:
            pywikibot.output("Already notified the user")
            return
        pywikibot.output(u"Notifying user {}...".format(user))
        talk_page.put(text, summary=comment, minor=False)
    except pywikibot.LockedPage:
        pywikibot.output(u'Talk page blocked, skip.')


def check_users(conn, cursor, category, delta_minutes, notify=False):
    """
    Check the uploaders in the given category, and potentially notify them.
    """
    usernames = get_users(conn, cursor, category, delta_minutes)
    pywikibot_site = pywikibot.Site(u'commons', u'commons')
    pywikibot.output(u"There were {} uploaders in the last {} minutes...".format(len(usernames), delta_minutes))
    try:
        users = [pywikibot.User(pywikibot_site, username[0].decode('utf-8')) for username in usernames]
        non_emailable_users = [user for user in users if not user.isEmailable()]
        pywikibot.output(u"...and {} non-emailable users".format(len(non_emailable_users)))

        if notify:
            for user in non_emailable_users:
                try:
                    notify_user(user)
                except Exception as e:
                    pywikibot.error(u"Error when notifying user, skipping")
                    continue
    except Exception as e:
        pass


def main():
    conn = None
    cursor = None
    delta_minutes = None
    category = None

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-delta':
            delta_minutes = int(value)
        elif option == '-category':
            category = value
        else:
            raise Exception(
                u'Bad parameters. Expected "-category", "-delta" or '
                u'pywikibot args. Found "{}"'.format(arg))
    if category and delta_minutes:
        (conn, cursor) = connect_to_commons_database()
        check_users(conn, cursor, category, delta_minutes, notify=True)
        close_database_connection(conn, cursor)
    else:
        pywikibot.error("Not enough arguments")


if __name__ == "__main__":
    main()
