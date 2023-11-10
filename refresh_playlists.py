import plexapi.exceptions
from plexapi.myplex import MyPlexAccount
from datetime import date
import logging
import configparser
import random

plex_config = configparser.ConfigParser()
plex_config.read("/plex_config.ini")

TODAY = date.today()

logging.basicConfig(level=logging.INFO)


def connect_to_plex(username, password, server_name):
    """Connect to Plex"""

    account = MyPlexAccount(username, password)
    plex = account.resource(server_name).connect()

    return plex


def add_old_episodes_to_playlist(plex, library_name, show_name):
    """
    Grab the current show.
    Look at all episodes.
    If episode has never been viewed, add to playlist.
    Otherwise, if episode has not been viewed in last X number of days 
        as specified in the script config, add to playlist.
    """

    days = int(plex_config.get('plex_config', 'recently_played_days'))

    old_episodes_playlist = []
    plex_current_show = plex.library.section(library_name).get(show_name)

    for episode in plex_current_show.episodes():
        if not episode.lastViewedAt:
            old_episodes_playlist.append(episode)
        else:
            days_since_played = (TODAY - episode.lastViewedAt.date()).days
            if days_since_played > days:
                old_episodes_playlist.append(episode)
    random.shuffle(old_episodes_playlist)
    return old_episodes_playlist


def delete_existing_playlist(plex, playlist_name):
    """If playlist already exists, delete it."""

    existing_playlists = [playlist.title for playlist in plex.playlists()]
    logging.info(f'Found existing playlists: {existing_playlists}')
    if playlist_name in existing_playlists:
        logging.info(f'Deleting existing playlist: {playlist_name}')
        try:
            plex.playlist(playlist_name).delete()
        except plexapi.exceptions.BadRequest:
#             this is ok and a bug in plex api and causing 204 but no real error found
            logging.info(f'Ate 204 error but was able to delete the playlist')

def create_new_playlist(plex, playlist_name, old_episodes_playlist):
    """Create a new playlist and add all the old episodes to it"""

    plex.createPlaylist(playlist_name, old_episodes_playlist)


if __name__ == '__main__':
    tv_shows = plex_config.get('plex_config', 'tv_shows').split(',')

    plex = connect_to_plex(
        username=plex_config.get('plex_config', 'username'),
        password=plex_config.get('plex_config', 'password'),
        server_name=plex_config.get('plex_config', 'server_name')
    )

    for show in tv_shows:
        logging.info(f'Updating playlist for show: {show}...')
        old_episodes_playlist = add_old_episodes_to_playlist(
            plex,
            library_name=plex_config.get('plex_config', 'library_name'),
            show_name=show
            )
        delete_existing_playlist(plex, show)
        create_new_playlist(plex, show, old_episodes_playlist)
