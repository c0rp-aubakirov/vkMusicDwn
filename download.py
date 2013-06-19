# -*- coding: utf-8 -*-
import os
import re
import urllib2
import json
import time
#import parallel

def usersMusic(access_token, user_id, searching, search, artist, bitrate):
    url = "https://api.vk.com/method/audio.get?uids=" + str(user_id) + "&format=json&access_token=" + access_token
    u = urllib2.urlopen(url)
    file = open("playlist.json", "w")
    if not os.path.exists(search):
        os.makedirs(search)
    badquality = open(search + "/Bad Quality Songs.txt" + searching, "w")
    file.write(u.read())
    file.close()
    if artist == False:
        data = prepareData(False)
    else:
        data = prepareData(artist)
    total = len(data['response'])
    for i in range(0, total):
        artist = data['response'][i]['artist']
        title = data['response'][i]['title']
        duration = data['response'][i]['duration']
        url = data['response'][i]['url']
        file_size = data['response'][i]['aid']
        download(url, duration, artist, title, search, str(i + 1) + "/" + str(total), badquality, bitrate, file_size)

def firstLetter(data):
    """
    """
    tdata = data.split(' ')
    data = ''
    for d in tdata:
        if len(d) > 1:
            d = d[0][0].upper() + d[1:].lower()
            data = data + d + ' '
    return data.strip(' ')


def remSym(data):
    """
    This method cleans string 'data'.
    Removes unused symbols, unnecessary words.
    """
    temp = ''
    for i in data:
        if 0 < ord(i) < 127 or 1040 <= ord(i) <= 1103:# не работает с русскими чарами
            temp += i.encode('utf-8')
    data = temp
    temp = ''
    for i in "/\?*:|<>.\/\"[];&_":
        if i in data:
            tdata = data.split(i)
            for j in tdata:
                temp += j + ' '
            data = temp.strip()
        temp = ''
    tdata = data.split(' ')
    for i in tdata:
        if not i.lower().startswith("club") and not i.lower().startswith("soundtrack") and not i.lower().startswith(
            "ost")and not i.lower().startswith("vk"):
            temp = temp + i + ' '
    data = temp
    temp = ''
    data = data.strip(" -+=!?,@#%^&'")
    return data


def save(total, u, artist, song, fname, sec, file_size, file_name, bitrate, badquality):
    ### remove next "if" if not downloading some songs
    if file_size >25000000:
        if os.access(fname, os.F_OK):
            os.remove(fname)
            print "File \"" + artist + " - " + song + "\" has a very big size"
            badquality.writelines(str(artist) + " - " + str(song) + "\n")
    else:
        f = open(fname, 'wb')
        if sec == 0:
            sec = 150
        if (file_size * 8 / 1024 / int(sec) > int(bitrate)):
            file_size_dl = 0
            block_sz = 8192
            print "Downloading: \"%s\" MBytes: %s" % (file_name, file_size / 1024 / 1024)
            print total,
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
            f.close()
        else:
            if os.access(fname, os.F_OK):
                f.close()
                os.remove(fname)
                print "File \"" + artist + " - " + song + "\" in a bad quality"
                badquality.writelines(str(artist) + " - " + str(song) + "\n")


def download(url, sec, artist, song, search, total, badquality, bitrate, file_size):
    tempname = ''
    if not os.path.exists(search):
        os.makedirs(search)
    if len(artist + song) > 80:
        artist = artist[0:30]
        song = song[0:30]
    file_name = artist + " - " + song + ".mp3"
    fname = search + '/' + file_name
    u = urllib2.urlopen(url)
    if not os.access(fname, os.F_OK):
        save(total, u, artist, song, fname.strip(' -'), sec, file_size, file_name, bitrate, badquality)
    else:
        if os.stat(fname).st_size < file_size:
            os.remove(fname)
            save(total, u, artist, song, fname.strip(' -'), sec, file_size, file_name, bitrate, badquality)
    fname = ''


def doSearch(access_token, user_id, scount, searching, search, offset, artist, bitrate):
    if len(str(offset)) == 0:
        offset=0
    url = "https://api.vk.com/method/audio.search?uids=" + str(user_id) + "&q=" + searching + "&offset=" + str(
        offset) + "&format=json&count=" + str(scount) + "&access_token=" + access_token
    connection = True
    while(connection):
        try:
            u = urllib2.urlopen(url)
            file = open("playlist.json", "w")
            if not os.path.exists(search):
                os.makedirs(search)
            badquality = open(search + "/Bad Quality Songs.txt" + searching, "w")
            file.write(u.read())
            file.close()
            if artist == False:
                start_time = time.time()
                data = prepareData(False)
                print "Time elapsed for analyze response: ", time.time() - start_time, "s"
            else:
                start_time = time.time()
                data = prepareData(artist)
                print "Time elapsed for analyze response: ", time.time() - start_time, "s"
            total = len(data['response'])
            for i in range(0, total):
                artist = data['response'][i]['artist']
                title = data['response'][i]['title']
                duration = data['response'][i]['duration']
                url = data['response'][i]['url']
                file_size = data['response'][i]['aid']
                download(url, duration, artist, title, search, str(i + 1) + "/" + str(total), badquality, bitrate, file_size)
            badquality.close()
            connection = False
        except urllib2.HTTPError, e:
            print e.code
            print e.msg
            print e.headers
            print e.fp.read()
            print "Please Wait for URL"
        time.sleep(5)

def findNormalDuration(dur,data,numbers,total):
    """
    This method finds average duration of song
    This is useful if song has many mixes
    and covers.
    """
    left=0
    right=0
    averageDur=0.0
    if len(dur) != 0:
        for i in dur:
            averageDur = averageDur + float(i)/ len(dur)
        for i in dur:
            if int(i) <= averageDur:
                left+=1
            else:
                right+=1
        if left>right:
            for j in range(0, total):
                if data['response'][j]['duration'] > averageDur:
                    if not j in numbers:
                        numbers.append(j)
        else:
            for j in range(0, total):
                if data['response'][j]['duration'] <= averageDur:
                    if not j in numbers:
                        numbers.append(j)
    return numbers

def prepareData(reject):
    """
    Obtained list of songs preparations.
    Removing similar songs, mixes.
    """
    numbers = []
    dur = []
    json_data = open('playlist.json')
    data = json.load(json_data)
    json_data.close()
    data['response'].pop(0)
    total = len(data['response'])
    print "List of music obtained\n"
    print "Analysing..."
    for i in range(0, total):
        artist = data['response'][i]['artist'].split('(')[0].split('[')[0].strip(' |[]()-=<>')
        title = data['response'][i]['title'].split('(')[0].split('[')[0].strip(' |[]()-=<>')
        data['response'][i]['artist'] = firstLetter(re.sub(' +', ' ', remSym(artist)))
        data['response'][i]['title'] = firstLetter(re.sub(' +', ' ', remSym(title)[0:50]))
        if reject != False:
            if artist.lower() != reject.lower() and i not in numbers:
                numbers.append(i)
            dur.append(data['response'][i]['duration'])
    #Deleting of not original songs
    for j in range(0, total):
        for i in data['response'][j]['title'].split(' '):
            if i.lower().startswith('remix')  or i.lower().startswith('dj') \
            or i.lower()=='dj' or i.lower()=='mix' or i.lower()=='http':
                #or i.lower().startswith('new')
                if not j in numbers:
                    numbers.append(j)
    if reject != False:
        numbers=findNormalDuration(dur,data,numbers,total)
    ### After popping i will check file size
    ### So less files => less queries need
    numbers.sort()
    for i in range(len(numbers)):
        data['response'].pop(numbers[i] - i)
    numbers = []
    total = len(data['response'])
    ### Parallel size checking
    ###
    #total, data = parallel.doInParallel(getSizeP, total, data, numbers)
    ###
    total,data=getSize(total,data,numbers)
    ### Remove all similar song from download list
    if reject == False:
        for i in range(0, total):
            if not i in numbers:
                ai = data['response'][i]['artist']
                ti = data['response'][i]['title']
                f_si = data['response'][i]['aid']
                for j in range(0, total):
                    if not j in numbers:
                        aj = data['response'][j]['artist']
                        tj = data['response'][j]['title']
                        f_sj = data['response'][j]['aid']
                        if ai.lower() == aj.lower() and ti.lower() == tj.lower() and i != j:
                            if f_si >= f_sj:
                                if not j in numbers:
                                    numbers.append(j)
                            else:
                                if not i in numbers:
                                    numbers.append(i)
    numbers.sort()
    for i in range(len(numbers)):
        data['response'].pop(numbers[i] - i)
    return data


def getSize(total, data, numbers):
    """
    Get size of song
    """
    for i in range(0, total):
        url = data['response'][i]['url']
        try:
            u = urllib2.urlopen(url)
        except:
            print 'Check your internet connection'
            data['response'][i]['aid'] = 25000001
            for i in range(len(numbers)):
                data['response'].pop(numbers[i] - i)
            total = len(data['response'])
            return total, data
        meta = u.info()
        fsize = int(meta.getheaders("Content-Length")[0])
        data['response'][i]['aid'] = fsize
        if fsize < 1500000 and i not in numbers:
            numbers.append(i)
            #print "Added " + str(i) + " on fsize"
    for i in range(len(numbers)):
        data['response'].pop(numbers[i] - i)
    total = len(data['response'])
    return total, data

def getSizeP(total, data, numbers, p, s):
    """
    Get size of song. Parallel version
    Need package parallel been imported
    import parallel
    """
    debug = 0
    try:
        for i in range(s, total, p):
            debug = i
            url = data['response'][i]['url']
            u = urllib2.urlopen(url)
            meta = u.info()
            fsize = int(meta.getheaders("Content-Length")[0])
            data['response'][i]['aid'] = fsize
            if fsize <= 1500000 and i not in numbers:
                numbers.append(i)
        for i in range(0, len(numbers)):
            data['response'].pop(numbers[i] - i)
        total = len(data['response'])
        numbers = []
        debug = True
        return total, data, numbers, False
    except urllib2.HTTPError, e:
        print e.code
        print e.msg
        print e.headers
        print e.fp.read()
        print "Please Wait. Connection problem."
        time.sleep(5)
        return 0, 0, debug, True
