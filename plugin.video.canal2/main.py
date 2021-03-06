# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import sys
from urllib import urlencode
from urlparse import parse_qsl

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from canal2 import stream_url_extractor

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


_resources_path = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources');
# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {'Live': [{'name': 'Canal2',
                       # 'thumb': 'http://www.canal2international.net/images/logo.png',
                       'icon': os.path.join(_resources_path ,'canal2logo_white_background.png'),
                       'thumb': os.path.join(_resources_path ,'canal2logo.png'),
                       'channel': stream_url_extractor.LIVE,
                       'genre': 'Mixed'},
                      ]
          }


            # 'Replay': [{'name': 'Postal Truck',
            #           'thumb': 'http://www.vidsplay.com/vids/us_postal.jpg',
            #           'videopage': 'http://www.vidsplay.com/vids/us_postal.mp4',
            #           'genre': 'Cars'}
            #          ]}


def build_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    return VIDEOS.iterkeys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or server.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        if len(VIDEOS[category]) == 1:
            add_video_list_item(VIDEOS[category][0])
        else:
            add_category_list_item(category)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def add_category_list_item(category):
    list_item = xbmcgui.ListItem(label=category)
    # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
    # Here we use the same image for all items for simplicity's sake.
    # In a real-life plugin you need to set each image accordingly.
    # Hier komen categorie plaatjes uit het eerste item in de categorie.
    # Wellicht aparte plaatjes voor categorie als we meer categorien hebben.
    list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                      'icon': VIDEOS[category][0]['icon'],
                      'fanart': VIDEOS[category][0]['thumb'],
                      'banner': VIDEOS[category][0]['thumb']})
    # Set additional info for the list item.
    # Here we use a category name for both properties for for simplicity's sake.
    # setInfo allows to set various information for an item.
    # For available properties see the following link:
    # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
    list_item.setInfo('video', {'title': category, 'genre': category})
    # Create a URL for a plugin recursive call.
    # Example: plugin://plugin.video.canal2/?action=listing&category=Animals
    url = build_url(action='listing', category=category)
    # is_folder = True means that this item opens a sub-list of lower level items.
    is_folder = True
    # Add our item to the Kodi virtual folder listing.
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        add_video_list_item(video)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def add_video_list_item(video):
    # Create a list item with a text label and a thumbnail image.
    list_item = xbmcgui.ListItem(label=video['name'])
    # Set additional info for the list item.
    list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
    # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
    # Here we use the same image for all items for simplicity's sake.
    # In a real-life plugin you need to set each image accordingly.
    list_item.setArt({'thumb': video['icon'], 'icon': video['icon'], 'fanart': video['thumb'], 'banner': video['thumb']})
    # Set 'IsPlayable' property to 'true'.
    # This is mandatory for playable items!
    list_item.setProperty('IsPlayable', 'true')
    # Create a URL for a plugin recursive call.
    # Example: plugin://plugin.video.canal2/?action=play&video=http://canal2-live-b2-cdn.hexaglobe.net/c9391...
    url = build_url(action='play', channel=video['channel'])
    # Add the list item to a virtual Kodi folder.
    # is_folder = False means that this item won't open any sub-list.
    is_folder = False
    # Add our item to the Kodi virtual folder listing.
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


def play_video(channel):
    """
    Play a video by the provided channel.
    Channel is resolved to a url before play
    Available channels in 

    :param channel: Canal2 channel: int
    :type path: str
    """
    xbmc.log("play_video called with channel: " + str(channel), level=xbmc.LOGDEBUG)
    url = stream_url_extractor.get_video_stream_url(channel)
    xbmc.log("channel resolved to play url: " + url, level=xbmc.LOGDEBUG)
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    # TODO: aspect ratio voor livestream klopt niet. Kunnen we player view mode
    # 16:9 stretch forceren?



def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    xbmc.log('[plugin.video.canal2] - router called with params ' + paramstring)
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video for provided channel. Url will be looked up before play
            play_video(int(params['channel']))
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    xbmc.log('[plugin.video.canal2] Plugin called', level=xbmc.LOGDEBUG)
    xbmc.log('[plugin.video.canal2] With arguments: ' + ';'.join(sys.argv), level=xbmc.LOGDEBUG)
    router(sys.argv[2][1:])
