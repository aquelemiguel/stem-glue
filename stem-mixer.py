import re
from pathlib import Path
from pydub import AudioSegment

class Stem:
    def __init__(self, path: str):
        self.path = path

    def get_audio_segment(self) -> AudioSegment:
        return AudioSegment.from_file(f'input/{self.path}')

class Track:
    def __init__(self, name: str, format: str):
        self.name = name
        self.format = format
        self.stems = []
        self.mixed = None

    def add_stem(self, stem: Stem):
        self.stems.append(stem)

    def combine(self) -> AudioSegment:
        mixed = self.stems[0].get_audio_segment()

        for stem in self.stems[1:]:
            mixed = mixed.overlay(stem.get_audio_segment())

        self.mixed = mixed

    def export(self):
        Path('output').mkdir(parents=True, exist_ok=True)
        self.mixed.export(f'output/{self.name}.{self.format}', format=self.format)

class Mixer:
    def __init__(self):
        self.tracks = {}
    
    def add_track(self, track: Track):
        self.tracks[track.name] = self.tracks.get(track.name, track)

    def mix(self):
        for track in self.tracks.values():
            track.combine()

    def export(self):
        for track in self.tracks.values():
            track.export()

expr = r"(.+)_(?:\d+)\.(.+)"
mixer = Mixer()

for path in Path('input').glob('*'):
    (name, format) = re.search(expr, path.name).groups()
    mixer.add_track(Track(name, format))
    mixer.tracks[name].add_stem(Stem(path.name))

mixer.mix()
mixer.export()
