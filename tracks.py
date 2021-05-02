from datetime import datetime
from pathlib import Path
from typing import TextIO, Iterable, ContextManager

from pydantic.main import BaseModel
from contextlib import contextmanager

default_path = Path(__file__).parent
tracks_path = default_path / 'tracks.ndjson'


class Identifiable(BaseModel):
    id: str
    name: str

    class Config:
        extra = 'ignore'
        frozen = True


class Track(Identifiable):
    album: Identifiable
    artists: list[Identifiable]
    added_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }


class TrackWriter:
    def __init__(self, f: TextIO):
        self.f = f

    def write_track(self, track: Track):
        self.f.write(track.json() + '\n')


class TrackReader:
    def __init__(self, f: TextIO):
        self.f = f

    def stream_tracks(self) -> Iterable[Track]:
        for line in self.f:
            yield Track.parse_raw(line)


@contextmanager
def track_writer() -> ContextManager[TrackWriter]:
    with open(tracks_path, 'w') as f:
        yield TrackWriter(f)


@contextmanager
def track_reader() -> ContextManager[TrackReader]:
    with open(tracks_path, 'r') as f:
        yield TrackReader(f)


def already_dumped() -> bool:
    return tracks_path.is_file() and tracks_path.stat().st_size > 0
