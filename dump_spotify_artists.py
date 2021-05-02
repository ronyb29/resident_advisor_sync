from typing import Iterable, Callable, TypeVar

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from tracks import Track, track_writer

T = TypeVar('T')


def _parse_saved_tracks_chunk(results) -> Iterable[Track]:
    for item in results['items']:
        track = Track(added_at=item['added_at'], **item['track'])
        yield track


class SpotifyDumper:
    def __init__(self):
        self.sp = Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

    def dump_saved_songs(self, spotify_user_id: str):
        with track_writer() as w:
            for track in self._get_liked_artists():
                w.write_track(track)

    def _get_liked_artists(self) -> Iterable[Track]:
        results = self.sp.current_user_saved_tracks()
        yield from self._consume_all(_parse_saved_tracks_chunk, results)

    def _consume_all(self, parser: Callable[[dict], Iterable[T]], result: dict) -> Iterable[T]:
        yield from parser(result)
        while result['next']:
            result = self.sp.next(result)
            yield from parser(result)
