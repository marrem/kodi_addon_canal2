from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup
import re

# TODO: null checks (ipv gechainde methods...)
import xbmc

LIVE = 1
INFO = 2
MUSIC = 3
MOVIES = 4

LIVE_PAGE = 'http://www.canal2international.net/live.php'
# INFO_PAGE


def get_video_stream_url(channel):
    xbmc.log("get_video_stream called with channel: " + str(channel), level=xbmc.LOGDEBUG)
    if (channel == LIVE):
        return get_video_stream_url_live()
    else:
        message = "Channel '" + channel + "' not found"
        xbmc.log(message)
        raise Exception(message)


def get_video_stream_url_live():
    xbmc.log("get_video_stream called with arguments: '" + LIVE_PAGE + "'")
    main_page = urlopen(LIVE_PAGE)
    player_page_url = parse_player_url(main_page)
    player_page = urlopen(player_page_url)
    return parse_stream_url(player_page)


def parse_stream_url(html):
    """
    Obtain m3u url from player page
    :param html player page:
    :return the m3u url:
    """
    tree = BeautifulSoup(html)
    script = tree.body.script.string
    stream_url_re = re.compile(r"player_hls\(\"(.*?)\"\);")
    stream_url = stream_url_re.search(script).group(1)
    return stream_url


def parse_player_url(html):
    """
    Obtain player iframe html page url from main live.php page
    :param html main page:
    :return the player page url:
    """
    tree = BeautifulSoup(html)
    # Assuming the link to the stream url is the src attribute of the first iframe
    stream_url = tree.iframe['src']
    return stream_url
