import sys
import xbmc
from lib.parser import kodi_log, viewitems


def play_using():
    dbtype = sys.listitem.getVideoInfoTag().getMediaType()

    params = None
    if dbtype == 'movie':
        params = {
            'play': 'movie',
            'tmdb_id': sys.listitem.getUniqueID('tmdb'),
            'imdb_id': sys.listitem.getUniqueID('imdb'),
            'query': sys.listitem.getVideoInfoTag().getTitle() or sys.listitem.getLabel(),
            'year': sys.listitem.getVideoInfoTag().getYear()
        }
    elif dbtype == 'episode':
        params = {
            'play': 'tv',
            'query': sys.listitem.getVideoInfoTag().getTVShowTitle(),
            'season': sys.listitem.getVideoInfoTag().getSeason(),
            'episode': sys.listitem.getVideoInfoTag().getEpisode()
        }

    if not params:
        return

    path = 'plugin.video.themoviedb.helper'
    for k, v in viewitems(params):
        if not v:
            continue
        path = '{},{}={}'.format(path, k, v)
    path = u'RunScript({})'.format(path)

    xbmc.executebuiltin(path)
    kodi_log(['TMDbHelper.Context: Executed Play Using\n', path], 1)
