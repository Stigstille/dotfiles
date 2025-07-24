#!/usr/bin/env bash

WALLPAPER_DIR="$HOME/Pictures/Backgrounds"
CURRENT_WALL=$(swww query | grep "image" | head -1 | awk -F': ' '{print $5}')

# Get a random wallpaper that is not the current one
WALLPAPER=$(find "$WALLPAPER_DIR" -type f ! -name "$(basename "$CURRENT_WALL")" ! -name $(basename "main.py") | shuf -n 1)
echo $WALLPAPER
# Apply the selected wallpaper
# swww img $WALLPAPER --transition-type random --transition-angle 25
swww img --transition-type wave $WALLPAPER --transition-fps 120 --transition-angle 25
WALLPAPERESCAPED=$(echo "$WALLPAPER" | sed 's/\//\\\//g')
echo "Done!"
/usr/bin/sed -i --follow-symlinks "s/path = .*/path = "$WALLPAPERESCAPED"/1" $HOME/.config/hypr/hyprlock.conf > /tmp/sed.log 2>&1
