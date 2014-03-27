#!/bin/bash
cd ~/.xbmc/addons/plugin.video.plurkTrend/
python -m youtube_dl "http://www.youtube.com/watch?v=$1" -g
