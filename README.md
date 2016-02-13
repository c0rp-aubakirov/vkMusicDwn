vkMusicDwn
==========

Vkontakte music downloader

Download music from vkontakte.ru, vk.com

1. Download your vkontakte playlist
2. Script not downloading what was already downloaded. If you update your playlist in vk.com, you can just choose "Download user playlist", and script will find new songs and download them.
3. Download songs using vk search. 
4. Download only songs that >=230 bitrate. If songs in your playlist are lower than 230, script will find this songs with better bitrate automatically

Requirements: Python 2.7

How to use:
Download files https://github.com/c0rp-aubakirov/vkMusicDwn/archive/master.zip

1. Extract files to folder some folder
2. Open file vkMusicDwn.py in any editor and put you login and password
3. Open terminal emulator and enter:
   python vkMusicDwn.py


if you want to download your playlist, enter yes:

    Download users playlist? ( yes/no ): yes


If you want to download something custom, this is how it works:
Suppose you want to download songs of Metallica band, but you don't know any songs names:

    Download users playlist? ( yes/no ): no
    What do want to find: Metallica
    How many songs do want to download: 10
    Put offset: 0


This will download first 10 songs, of Metallica band, that is appear in vk.com music database with "Metallica" as search word
