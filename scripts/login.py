#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Script to log the robot in to a wiki account.

Suggestion is to make a special account to use for robot use only. Make
sure this robot account is well known on your home wiki before using.

Parameters:

   -all         Try to log in on all sites where a username is defined in
                user-config.py.


   -force       Ignores if the user is already logged in, and tries to log in.

   -pass        Useful in combination with -all when you have accounts for
                several sites and use the same password for all of them.
                Asks you for the password, then logs in on all given sites.

   -pass:XXXX   Uses XXXX as password. Be careful if you use this
                parameter because your password will be shown on your
                screen, and will probably be saved in your command line
                history. This is NOT RECOMMENDED for use on computers
                where others have either physical or remote access.
                Use -pass instead.

   -sysop       Log in with your sysop account.

If not given as parameter, the script will ask for your username and
password (password entry will be hidden), log in to your home wiki using
this combination, and store the resulting cookies (containing your password
hash, so keep it secured!) in a file in the data subdirectory.

All scripts in this library will be looking for this cookie file and will
use the login information if it is present.

To log out, throw away the *.lwp file that is created in the data
subdirectory.
"""
#
# (C) Rob W.W. Hooft, 2003
# (C) Pywikipedia bot team, 2003-2012
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import logging
import pywikibot
from os.path import join
from pywikibot import config, deprecate_arg
from pywikibot.exceptions import NoSuchSite, NoUsername


def main(*args):
    password = None
    sysop = False
    logall = False
    for arg in pywikibot.handleArgs(*args):
        if arg.startswith("-pass"):
            if len(arg) == 5:
                password = pywikibot.input(u'Password for all accounts:',
                                           password=True)
            else:
                password = arg[6:]
        elif arg == "-sysop":
            sysop = True
        elif arg == "-all":
            logall = True
        elif arg == "-force":
            pywikibot.output(u"To force a re-login, please delete the revelant lines from '%s' (or the entire file) and try again." %
                             join(config.base_dir, 'pywikibot.lwp'))
        else:
            pywikibot.showHelp('login')
            return
    if logall:
        if sysop:
            namedict = config.sysopnames
        else:
            namedict = config.usernames
    else:
        site = pywikibot.getSite()
        namedict = {site.family.name: {site.lang: None}}
    for familyName in namedict:
        for lang in namedict[familyName]:
            try:
                site = pywikibot.getSite(code=lang, fam=familyName)
                site.login()

                user = site.user()
                if user:
                    pywikibot.output(u"Logged in on %(site)s as %(user)s." % locals())
                else:
                    pywikibot.output(u"Not logged in on %(site)s." % locals())
            except NoSuchSite:
                pywikibot.output(u'%s.%s is not a valid site, please remove it'
                                 u' from your config' % (lang, familyName))
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
