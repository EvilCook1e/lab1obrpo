import struct
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Record:
    name: str
    score: int
    MAX_NAME_LENGTH: int = 20

    def __post_init__(self):
        if len(self.name) > self.MAX_NAME_LENGTH:
            self.name = self.name[:self.MAX_NAME_LENGTH]


class ScoreBoard:
    def __init__(self, filename: str = "records.dat", max_records: int = 10):
        self.filename = filename
        self.max_records = max_records
        self.records: List[Record] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self.records = []
            return

        self.records = []

        try:
            with open(self.filename, 'rb') as f:
                while True:
                    name_bytes = f.read(40)
                    score_bytes = f.read(4)

                    if len(name_bytes) < 40 or len(score_bytes) < 4:
                        break

                    try:
                        name = name_bytes.decode('utf-16le').rstrip('\x00')
                    except UnicodeDecodeError:
                        continue

                    score = struct.unpack('<i', score_bytes)[0]
                    self.records.append(Record(name=name, score=score))
        except (IOError, struct.error):
            self.records = []

        self._sort()

    def _save(self) -> None:
        try:
            with open(self.filename, 'wb') as f:
                for record in self.records[:self.max_records]:
                    name_encoded = record.name.encode('utf-16le')
                    name_padded = name_encoded.ljust(40, b'\x00')
                    score_encoded = struct.pack('<i', record.score)
                    f.write(name_padded)
                    f.write(score_encoded)
        except IOError:
            pass

    def _sort(self) -> None:
        self.records.sort(key=lambda r: r.score, reverse=True)

    def add_record(self, name: str, score: int) -> bool:
        if not self.is_high_score(score):
            return False

        new_record = Record(name=name, score=score)
        self.records.append(new_record)
        self._sort()

        if len(self.records) > self.max_records:
            self.records = self.records[:self.max_records]

        self._save()
        return True

    def is_high_score(self, score: int) -> bool:
        if len(self.records) < self.max_records:
            return True
        return score > self.records[-1].score

    def get_rank(self, score: int) -> Optional[int]:
        if not self.is_high_score(score):
            return None

        rank = 1
        for record in self.records:
            if score > record.score:
                return rank
            rank += 1
        return rank if rank <= self.max_records else None

    def get_records(self) -> List[Record]:
        return self.records.copy()

    def clear(self) -> None:
        self.records = []
        self._save()