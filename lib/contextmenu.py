import sys
import xbmc
from lib.parser import kodi_log, viewitems, try_encode, try_decode


def play_using():
    dbtype = sys.listitem.getVideoInfoTag().getMediaType()

    params = None
    if dbtype == 'movie':
        params = {
            'play': 'movie',
            'tmdb_id': sys.listitem.getUniqueID('tmdb'),
            'imdb_id': sys.listitem.getUniqueID('imdb'),
            'query': sys.listitem.getVideoInfoTag().getTitle() or sys.listitem.getLabel(),
            'year': sys.listitem.getVideoInfoTag().getYear(),
            'ignore_default': 'true'
        }
    elif dbtype == 'episode':
        params = {
            'play': 'tv',
            'query': sys.listitem.getVideoInfoTag().getTVShowTitle(),
            'season': sys.listitem.getVideoInfoTag().getSeason(),
            'episode': sys.listitem.getVideoInfoTag().getEpisode(),
            'ignore_default': 'true'
        }

    if not params:
        return

    path = 'plugin.video.themoviedb.helper'
    for k, v in viewitems(params):
        if not v:
            continue
        path = u'{},{}={}'.format(path, k, try_decode(v))
    path = u'RunScript({})'.format(path)

    xbmc.executebuiltin(try_encode(try_decode(path)))
    kodi_log(['TMDbHelper.Context: Executed Play Using\n', path], 1)
