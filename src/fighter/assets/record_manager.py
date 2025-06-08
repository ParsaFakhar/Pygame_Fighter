import json
import os
from datetime import datetime
from src.fighter.core.enums import RecordField
from src.fighter.core.constants import *
from typing import List, Dict, Any, Optional


class RecordManager:
    def __init__(self,
                 path: str = DEFAULT_RECORD_PATH,
                 max_records: int = DEFAULT_MAX_RECORDS,
                 timestamp_func: Optional[callable] = None
                 ):
        self.path = path
        self.max_records = max_records
        # default to UTC ISO timestamps
        self.timestamp_func = timestamp_func or (lambda: datetime.utcnow().isoformat())
        self.records: List[Dict[str, Any]] = self._load()
        self.records = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding=UTF_8) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def add(self, score: int, level: int):
        """Append a new record with timestamp."""
        entry = {
            RecordField.TIMESTAMP.value: self.timestamp_func(),
            RecordField.SCORE.value: score,
            RecordField.LEVEL.value: level,
        }
        self.records.append(entry)
        # optional: keep only top N by score
        self.records.sort(key=lambda e: e[RecordField.SCORE.value], reverse=True)
        self.records = self.records[:self.max_records]  # top 10

    def save(self):
        with open(self.path, "w", encoding=UTF_8) as f:
            json.dump(self.records, f, indent=2)

    def get_top(self, n):
        if n is None or n > len(self.records):
            return self.records[:]
        return self.records[:n]
