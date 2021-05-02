import os
from itertools import groupby
from pprint import pprint

from dump_spotify_artists import SpotifyDumper
from tracks import already_dumped, track_reader


def main():
    user_id = os.environ['spotify_user_id']  # TODO: move to args

    if not already_dumped():
        s = SpotifyDumper()
        s.dump_saved_songs(spotify_user_id=user_id)

    with track_reader() as tr:
        tracks = list(tr.stream_tracks())

    artists = {
        a.name
        for t in tracks
        for a in t.artists
    }

    print(len(artists))
    pprint(artists)


if __name__ == '__main__':
    main()
