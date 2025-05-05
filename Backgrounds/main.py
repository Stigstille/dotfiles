#!/usr/bin/env python

import logging
import time
import traceback
from ytmusicapi import YTMusic
import os, re, requests

ytmusic = YTMusic()

previusSong = ""

log_file = os.path.expanduser('~/crash_log.txt')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    previusSong = ""
    while True: 
        song = os.popen('playerctl metadata --format "{{title}} - {{artist}}"').read()
        if (previusSong != song) and (song != ""):
            previusSong = song
            logging.info(f"Song changed to {song}")
            try: 
                search_results = ytmusic.search(song,"songs")

                videoId = search_results[0]["videoId"]
            except:
                search_results = ytmusic.search(song)
                logging.warning(f"Song not found, searching for {search_results[0]['title']} instead")
                videoId = search_results[0]["videoId"]
            logging.debug(f"Video ID: {videoId}")
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

            os.system(r'/usr/bin/sed -i --follow-symlinks "s/path = .*/path = \/tmp\/album-art.jpg/1" $HOME/.config/hypr/hyprlock.conf')
            
            os.system('swww img /tmp/album-art.jpg --transition-type random --transition-angle 25')
        elif (previusSong != song) and (song == ""):
            previusSong = song
            logging.info(f"No song playing")
            os.system("~/.config/hypr/reloadHyprpaper.sh")
        time.sleep(1)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(f'An error occurred: {str(e)}')
            raise