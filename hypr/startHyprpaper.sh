#!/usr/bin/env bash

swww-daemon 
sleep 1

WALLPAPER_DIR="$HOME/Pictures/Backgrounds/"
CURRENT_WALL=$(swww query | grep "image" | head -1 | awk -F': ' '{print $5}')

# Get a random wallpaper that is not the current one
WALLPAPER=$(find "$WALLPAPER_DIR" -type f ! -name "$(basename "$CURRENT_WALL")" | shuf -n 1)

# Apply the selected wallpaper
swww img $WALLPAPER --transition-type random --transition-angle 25
