#!/usr/bin/env python

from ytmusicapi import YTMusic
import os, re, requests

ytmusic = YTMusic()

previusSong = ""

while True: 
    song = os.popen('playerctl metadata --format "{{title}} - {{artist}}"').read()
    if (previusSong != song) and (song != ""):
        previusSong = song
        try: 
            search_results = ytmusic.search(song,"songs")

            videoId = search_results[0]["videoId"]
        except:
            search_results = ytmusic.search(song)
            videoId = search_results[0]["videoId"]
        thumbnailInfo = search_results[0]["thumbnails"][0]
        print(search_results[0]["title"])
        thumbnail = thumbnailInfo["url"]
        thumbnailWidth = thumbnailInfo["width"]
        thumbnailHeight = thumbnailInfo["height"]

        # please ignore my shitty regex
        pattern = r"=w.{1,4}\-h.{1,4}-"
        size = f"=w{thumbnailWidth*100}-h{thumbnailHeight*100}-"

        thumbnailResized = re.sub(pattern, size, thumbnail)
        img_data = requests.get(thumbnailResized).content
        with open('/tmp/album-art.jpg', 'wb') as handler:
            handler.write(img_data)
        
        os.system('swww img /tmp/album-art.jpg --transition-type random --transition-angle 25')
    elif (previusSong != song) and (song == ""):
        previusSong = song
        os.system("~/.config/hypr/reloadHyprpaper.sh")
