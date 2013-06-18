# -*- coding: utf-8 -*-
import download
import vk_auth
import urllib2
import os
import time
import getpass


# Path to download folder
dpath = '/music/'

### Uncomment this if you want put email and
### password from keyboard
email = raw_input("Email: ")
password = getpass.getpass()

### This block for static email and password
###
#email = 'email'
#password = 'password'

usersmusic = raw_input("Download users playlist? ( yes/no ): ")
if usersmusic.lower() == "n" or usersmusic.lower() == "no":
    # different search can be splitted by '|'.
    search = download.firstLetter(raw_input("What do want to find: ")).decode('utf-8')
    scount = raw_input("How many songs do want to download: ")
    offset = raw_input("Put offset: ")
    start_time = time.time()
    for s in search.split('|'):
        searching = urllib2.quote(s.encode('utf-8'))
        s = download.remSym(s)
        access_token, user_id = vk_auth.auth(email, password, "3164037", "10")
        download.doSearch(access_token, user_id, scount, searching, dpath + s, offset, False)
        bq = open(dpath + s + "/Bad Quality Songs.txt" + searching, 'r')
        bqlist = bq.readlines()
        bq.close()
        for i in bqlist:
            download.doSearch(access_token, user_id, 7, urllib2.quote(i.strip()), dpath + s, 0, i.split(" - ")[0])
        if os.path.exists(dpath + s):
            for i in os.listdir(dpath + s + '/'):
                if i.startswith("Bad Quality Songs.txt"):
                    os.remove(dpath + s + "/" + i)
    print "Finish"
else:
    if usersmusic.lower() == "y" or usersmusic.lower() == "yes":
        access_token, user_id = vk_auth.auth(email, password, "3164037", "10")
        download.usersMusic(access_token, user_id, 'myplaylist', dpath + 'myplaylist', False)
        search = 'myplaylist'
        searching = 'myplaylist'
        bq = open(dpath + search + "/Bad Quality Songs.txt" + searching, 'r')
        bqlist = bq.readlines()
        bq.close()
        for i in bqlist:
            download.doSearch(access_token, user_id, 11, urllib2.quote(i.strip()), dpath + search, 0, i.split(" - ")[0])
        if os.path.exists(dpath + search):
            for i in os.listdir(dpath + search + '/'):
                if i.startswith("Bad Quality Songs.txt"):
                    os.remove(dpath + search + "/" + i)
        print "Finish"
    else:
        print "Please answer yes/y or no/n"
