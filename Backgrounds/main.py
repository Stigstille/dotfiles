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
            print(f"Song changed to {song}")
            file = os.path.expanduser(f'~/Public/album-art/{re.sub(r'[^a-zA-Z0-9 -]', '_', song)}.jpg')
            if not os.path.exists(file):
                try: 
                    search_results = ytmusic.search(song,"songs")
                    if (len(search_results) < 1):
                        raise ValueError("Empty List")
                    if ((search_results[0]["title"] == "Bad Gas") or ("Aquí Te Esperaré".lower() in search_results[0]["title"].lower())):
                        logging.warning(f"Annoying song found, skipping")
                        raise ValueError("Fuck \"Bad Gas\"")
                    videoId = search_results[0]["videoId"]
                except:
                    search_results = ytmusic.search(song)
                    logging.warning(f"Song not found, searching for video thumbnail instead")
                    if len(search_results) > 0:
                        title = search_results[0]["title"].lower()
                        if title == "bad gas".lower() or "aquí te esperaré" in title:
                            logging.warning(f"Annoying thumbnail found, skipping")
                            search_results = []

                    videoId = "N/A"
                    if (len(search_results) > 0):
                        videoId = search_results[0]["videoId"]
                logging.debug(f"Video ID: {videoId}")
                thumbnailResized = "https://album.stille.zip/unknown.jpg"
                if len(search_results) > 0:
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
                with open(file, 'wb') as handler:
                    handler.write(img_data)

            sed_cmd = f"""/usr/bin/sed -i --follow-symlinks 's|path = .*|path = {file}|' $HOME/.config/hypr/hyprlock.conf"""
            os.system(sed_cmd)
            
            # os.system('swww img /tmp/album-art.jpg --transition-type random --transition-angle 25')
            os.system(f"swww img --transition-angle 25 --transition-type wave '{file}' --transition-fps 120")
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
