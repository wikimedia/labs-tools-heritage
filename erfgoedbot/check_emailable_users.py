#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Check whether uploaders are emailable

Usage:
python check_emailable_users.py -delta:120 -category:Images_from_Wiki_Loves_Monuments_2018
"""
import datetime

import pywikibot

from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_commons_database
)


def get_usernames_from_database(conn, cursor, category, delta_minutes=120):
    """
    Retrieve the uploaders of images in the given category in the given timeframe.
    (Only registered users, since that’s a requirement to upload to  Wikimedia Commons)
    """
    pywikibot.output("Retrieving users...")
    query = (
        "SELECT"
        " user.user_name as uploader"
        " FROM (SELECT"
        "   cl_to,"
        "   cl_from"
        "   FROM categorylinks"
        "   WHERE cl_to = %s AND cl_type = 'file') cats"
        " INNER JOIN page ON cl_from = page_id"
        " INNER JOIN image ON page_title = img_name"
        " LEFT JOIN actor ON actor.actor_id = image.img_actor"
        " LEFT JOIN user ON user.user_id = actor.actor_user"
        " WHERE img_timestamp BETWEEN %s AND %s"
        " GROUP BY uploader")

    now = datetime.datetime.utcnow()

    formatter = "%Y%m%d%H%M%S"
    begin_time = (now + datetime.timedelta(minutes=0 - delta_minutes)).strftime(formatter)
    end_time = now.strftime(formatter)

    cursor.execute(query, (category, begin_time, end_time))

    result = cursor.fetchall()
    return [username[0] for username in result]


def get_non_emailable_users(usernames):
    """
    Return all non-emailable users among the given usernames.
    """
    pywikibot_site = pywikibot.Site('commons', 'commons')
    users = [pywikibot.User(pywikibot_site, username.decode('utf-8')) for username in usernames]
    return [user for user in users if not user.isEmailable()]


def notify_user(user):
    talk_page = user.getUserTalkPage()
    try:
        text = "{{subst:WLM-enable-email}}"
        summary = "Notifying WLM participant of missing e-mail address."
        history_users = [edit['user'] for edit in talk_page.getLatestEditors(limit=10)]
        if user.site.username() in history_users:
            pywikibot.output("Already notified the user")
            return
        pywikibot.output("Notifying user {}...".format(user))
        talk_page.text += text
        talk_page.save(summary=summary, minor=False)
    except pywikibot.LockedPage:
        pywikibot.output('Talk page blocked, skip.')


def notify_users(users):
    """
    Notify the given users.
    """
    for user in users:
        try:
            notify_user(user)
        except Exception as e:
            pywikibot.error("Error when notifying user {}, skipping".format(user))
            continue


def process(category, delta_minutes, notify=False):
    (conn, cursor) = connect_to_commons_database()
    usernames = get_usernames_from_database(conn, cursor, category, delta_minutes)
    close_database_connection(conn, cursor)
    pywikibot.output("There were {} uploaders in the last {} minutes...".format(len(usernames), delta_minutes))
    users = get_non_emailable_users(usernames)
    pywikibot.output("...and {} non-emailable users".format(len(users)))
    if notify:
        notify_users(users)


def main():
    conn = None
    cursor = None
    delta_minutes = None
    category = None
    notify = False

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-delta':
            delta_minutes = int(value)
        elif option == '-category':
            category = value
        elif option == '-notify':
            notify = True
        else:
            raise Exception(
                'Bad parameters. Expected "-category", "-delta", "-notify" or '
                'pywikibot args. Found "{}"'.format(arg))
    if category and delta_minutes:
        process(category, delta_minutes, notify=notify)
    else:
        pywikibot.error("Not enough arguments")


if __name__ == "__main__":
    main()
