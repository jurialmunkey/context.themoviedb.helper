import sys
import xbmc
from lib.parser import viewitems, try_encode, try_decode


def run_script(*args, **kwargs):
    path = 'plugin.video.themoviedb.helper'
    for i in args:
        if not i:
            continue
        path = u'{},{}'.format(path, i)
    for k, v in viewitems(kwargs):
        if not v:
            continue
        path = u'{},{}={}'.format(path, k, try_decode(v))
    path = u'RunScript({})'.format(path)
    xbmc.executebuiltin(try_encode(try_decode(path)))


def play_using(ignore_default=True):
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
            'episode': sys.listitem.getVideoInfoTag().getEpisode(),
        }
    if not params:
        return
    if ignore_default:
        params['ignore_default'] = 'true'
    run_script(**params)


def sync_trakt():
    # trakt_type, unique_id, season, episode, id_type
    dbtype = sys.listitem.getVideoInfoTag().getMediaType()
    params = None
    if dbtype in ['movie', 'tvshow']:
        params = {
            'tmdb_type': 'movie' if dbtype == 'movie' else 'tv',
            'tmdb_id': sys.listitem.getUniqueID('tmdb'),
            'imdb_id': sys.listitem.getUniqueID('imdb'),
            'query': sys.listitem.getVideoInfoTag().getTitle() or sys.listitem.getLabel(),
            'year': sys.listitem.getVideoInfoTag().getYear()}
    elif dbtype == 'episode':
        params = {
            'tmdb_type': 'tv',
            'query': sys.listitem.getVideoInfoTag().getTVShowTitle(),
            'season': sys.listitem.getVideoInfoTag().getSeason(),
            'episode': sys.listitem.getVideoInfoTag().getEpisode(),
            'episode_year': sys.listitem.getVideoInfoTag().getYear()}
    if not params:
        return
    run_script('sync_trakt', **params)
