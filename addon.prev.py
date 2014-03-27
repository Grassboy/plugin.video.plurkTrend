# -*- coding: UTF-8 -*-
import os
import sys
import time
import json
import urllib,urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])



def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
 
mode = args.get('mode', None)
 
if mode is None:
    xbmcplugin.setContent(addon_handle, 'movies')
    req = urllib2.Request("http://grassboy.tw/plurkTool/plurk_trend/plurkTrend_tr_ch1day.txt", None, {'user-agent':'grassboy/plurk_trend'})
    opener = urllib2.build_opener()
    data = opener.open(req)
    json_string = data.read();
    decoded = json.loads(json_string);
    it = iter(decoded)
    for video_id,video_name in zip(it, it):
      url = build_url({'mode': 'folder', 'video_id': video_id, 'video_name': json.dumps(video_name)})
      icon_img = 'http://i.ytimg.com/vi/' + video_id + '/2.jpg'
      fanart_img = 'https://i1.ytimg.com/vi/' + video_id + '/sddefault.jpg'
      li = xbmcgui.ListItem(video_name, iconImage=icon_img)
      li.setProperty('fanart_image', fanart_img)
      xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
 
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
 
elif mode[0] == 'folder':
    video_id = args['video_id'][0]
    video_name = json.loads(args['video_name'][0])
    txt = os.popen('sh '+os.getcwd()+'/tmp.sh "'+video_id+'"').readlines();
    url = txt[0]
    xbmc.Player().play(url)
    icon_img = 'http://i.ytimg.com/vi/' + video_id + '/1.jpg'
    fanart_img = 'https://i1.ytimg.com/vi/' + video_id + '/sddefault.jpg'
    li = xbmcgui.ListItem(u'開始播放【' + video_name + u'】', iconImage=icon_img)
    li.setProperty('fanart_image', fanart_img)
