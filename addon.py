# -*- coding: UTF-8 -*-
import urllib, urllib2, json, sys, xbmcplugin, xbmcgui, xbmcaddon
import HTMLParser
html_parser = HTMLParser.HTMLParser()

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def INDEX(list_url):
    xbmc.log(list_url)
    req = urllib2.Request(list_url, None, {'user-agent':'grassboy/plurk_trend'})
    opener = urllib2.build_opener()
    data = opener.open(req)
    json_string = data.read();
    decoded = json.loads(json_string);
    it = iter(decoded)
    url = build_url({'mode': 'other_list'})
    icon_img =  os.path.dirname(__file__) + '/otherlist.png'
    li = xbmcgui.ListItem('[COLOR 88FFFFFF](觀看其他來源...)[/COLOR]', iconImage=icon_img)
    li.setProperty('fanart_image', __settings__.getAddonInfo('fanart'))
    li.select(False)

    first = True
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
    for video_id,video_name in zip(it, it):
      addDownLink(video_id, html_parser.unescape(video_name), first)
      first = False
    

def VIDEOLINKS(video_id, video_name):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create(u'讀取中，請稍候', u'正在從 YouTube 取得影片連結…')
    pDialog.update(30, u'正在從 YouTube 取得影片連結…')
    txt = os.popen('sh '+os.getcwd()+'/tmp.sh "'+video_id+'"').readlines();
    url = txt[0]
    li = xbmcgui.ListItem(video_name)
    li.setInfo('video', {'Title': video_name})
    if not pDialog.iscanceled():
      pDialog.update(100, u'取得影片連結，開始播放')
      xbmc.Player().play(url, li)
      pDialog.close()

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param

def ADDLIST():
    new_id = xbmcgui.Dialog().input('請輸入要訂閱的 YouTube user id:')
    if new_id != '':
        youtube_list.append(new_id)
        __settings__.setSetting('youtube_list', ' '.join(youtube_list))
        xbmc.executebuiltin('Container.Refresh')
        

def OTHERLISTS():
    icon_img =  os.path.dirname(__file__) + '/plurk_list.png'
    url = build_url({'mode': 'set_list', 'list_name': '!PLURK_1HR!'})
    li = xbmcgui.ListItem('[COLOR FFFFAA00]Plurk 河道 一小時內 的熱門影片[/COLOR]', iconImage=icon_img)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)
    url = build_url({'mode': 'set_list', 'list_name': '!PLURK_6HR!'})
    li = xbmcgui.ListItem('[COLOR FFFFAA00]Plurk 河道 六小時內 的熱門影片[/COLOR]', iconImage=icon_img)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)
    url = build_url({'mode': 'set_list', 'list_name': '!PLURK_24HR!'})
    li = xbmcgui.ListItem('[COLOR FFFFAA00]Plurk 河道 二十四小時內 的熱門影片[/COLOR]', iconImage=icon_img)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)

    for list_name in youtube_list:
      addYoutubeListLink(list_name)

    icon_img =  os.path.dirname(__file__) + '/youtube_add.png'
    url = build_url({'mode': 'add_list'})
    li = xbmcgui.ListItem('[COLOR 66FFFFFF]  (將 YouTube 使用者加入清單...)  [/COLOR]', iconImage=icon_img)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)

def addYoutubeListLink(list_name):
    url = build_url({'mode': 'set_list', 'list_name': list_name})
    icon_img =  os.path.dirname(__file__) + '/youtube_list.png'
    li = xbmcgui.ListItem(list_name + u' 最近上傳的 YouTube 影片', iconImage=icon_img)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)

    return True

def addDownLink(video_id, video_name, first):
    url = build_url({'mode': 'play', 'video_id': video_id, 'video_name': json.dumps(video_name)})
    icon_img = 'http://i.ytimg.com/vi/' + video_id + '/2.jpg'
    fanart_img = 'https://i1.ytimg.com/vi/' + video_id + '/sddefault.jpg'
    li = xbmcgui.ListItem('[B]'+video_name+'[/B]', iconImage=icon_img)
    li.setProperty('fanart_image', fanart_img)
    li.select(first)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=False)

    return True

    

# -------------------------------------------------

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

__settings__ = xbmcaddon.Addon(id='plugin.video.plurkTrend')
youtube_list = __settings__.getSetting('youtube_list').strip().split(' ')
prev_list = __settings__.getSetting('prev_list')

topparams = get_params()
video_id = None
video_name = None
mode = None

try:
    video_id = urllib.unquote_plus(topparams["video_id"])
except:
    pass
try:
    video_name = json.loads(urllib.unquote_plus(topparams["video_name"]))
except:
    pass
try:
    mode = topparams["mode"]
except:
    pass

xbmc.log('NOW mode:'+str(mode))

if mode == 'set_list' or mode == None:
    try:
        list_name = topparams["list_name"]
    except:
        list_name = None;
        pass

    if list_name == None:
      list_name = __settings__.getSetting("prev_list")
    else:
      __settings__.setSetting("prev_list", list_name)
    if(mode == 'set_list'):
      xbmc.executebuiltin('Action(ParentDir)')
      xbmc.executebuiltin('Container.Refresh')
    else:
      if list_name == '!PLURK_1HR!':
        list_url = "http://grassboy.tw/plurkTool/plurk_trend/plurkTrend_tr_ch1hour.txt"
      elif list_name == '!PLURK_6HR!':
        list_url = "http://grassboy.tw/plurkTool/plurk_trend/plurkTrend_tr_ch6hours.txt"
      elif list_name == '!PLURK_24HR!':
        list_url = "http://grassboy.tw/plurkTool/plurk_trend/plurkTrend_tr_ch1day.txt"
      elif any(list_name in s for s in youtube_list):
        list_url = "http://grassboy.tw/plurkTool/plurk_trend/youtube_video.php?id=" + str(list_name)
      else:
        list_url = "http://grassboy.tw/plurkTool/plurk_trend/plurkTrend_tr_ch1day.txt"
        __settings__.setSetting("prev_list", '!PLURK_24HR!')

      INDEX(list_url)

elif mode == 'play':
    VIDEOLINKS(video_id, video_name)

elif mode == 'other_list':
    OTHERLISTS()

elif mode == 'add_list':
    ADDLIST()

elif mode == 'del_list':
    DELLIST()
    OTHERLISTS()

elif mode == 'move_list':
    OTHERLISTS()

xbmcplugin.endOfDirectory(addon_handle)
