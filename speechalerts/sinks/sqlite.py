"""SQLite audit log: every alert and every final transcript segment."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from speechalerts.config import settings
from speechalerts.models import Alert, TranscriptSegment

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at REAL NOT NULL,
    ended_at REAL,
    mode TEXT NOT NULL,
    source TEXT NOT NULL,
    title TEXT
);
CREATE TABLE IF NOT EXISTS alerts (
    id TEXT PRIMARY KEY,
    run_id INTEGER REFERENCES runs(id),
    parent_id TEXT,
    figure TEXT NOT NULL,
    state TEXT NOT NULL,
    entity TEXT NOT NULL,
    tickers TEXT NOT NULL,
    stance TEXT,
    action TEXT,
    quote TEXT,
    summary TEXT,
    confidence REAL,
    t_audio REAL,
    t_spoken REAL,
    t_stt REAL,
    t_llm REAL,
    t_alert REAL NOT NULL,
    latency_ms INTEGER,
    source TEXT,
    speaker TEXT,
    word_confidence REAL
);
CREATE INDEX IF NOT EXISTS alerts_t_alert ON alerts(t_alert);
CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER REFERENCES runs(id),
    t_audio_start REAL,
    t_audio_end REAL,
    t_wall REAL,
    confidence REAL,
    text TEXT NOT NULL,
    speaker_label TEXT
);
"""

# Columns added after the first release; applied with ALTER TABLE when missing.
_MIGRATIONS = [
    ("alerts", "speaker", "TEXT"),
    ("alerts", "word_confidence", "REAL"),
    ("segments", "speaker_label", "TEXT"),
]


class SqliteSink:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or settings.db_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        for table, column, ctype in _MIGRATIONS:
            cols = {row[1] for row in self.conn.execute(f"PRAGMA table_info({table})")}
            if column not in cols:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ctype}")
        self.conn.commit()
        self.run_id: int | None = None

    def start_run(self, mode: str, source: str, title: str = "") -> int:
        cur = self.conn.execute(
            "INSERT INTO runs (started_at, mode, source, title) VALUES (?, ?, ?, ?)",
            (time.time(), mode, source, title),
        )
        self.conn.commit()
        self.run_id = int(cur.lastrowid)
        return self.run_id

    async def alert(self, alert: Alert) -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO alerts
               (id, run_id, parent_id, figure, state, entity, tickers, stance, action, quote, summary,
                confidence, t_audio, t_spoken, t_stt, t_llm, t_alert, latency_ms, source, speaker, word_confidence)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                alert.id, self.run_id, alert.parent_id, alert.figure, alert.state.value, alert.entity,
                json.dumps(alert.tickers), alert.stance, alert.action, alert.quote, alert.summary,
                alert.confidence, alert.t_audio, alert.t_spoken, alert.t_stt, alert.t_llm, alert.t_alert,
                alert.latency_ms, alert.source, alert.speaker, alert.word_confidence,
            ),
        )
        self.conn.commit()

    async def segment(self, seg: TranscriptSegment) -> None:
        if not seg.is_final:
            return
        self.conn.execute(
            "INSERT INTO segments (run_id, t_audio_start, t_audio_end, t_wall, confidence, text, speaker_label) VALUES (?,?,?,?,?,?,?)",
            (self.run_id, seg.t_audio_start, seg.t_audio_end, seg.t_wall, seg.confidence, seg.text, seg.speaker_label),
        )
        self.conn.commit()

    def recent_alerts(self, limit: int = 100) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM alerts ORDER BY t_alert DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = [d[0] for d in self.conn.execute("SELECT * FROM alerts LIMIT 0").description]
        out = []
        for row in rows:
            rec = dict(zip(cols, row))
            rec["tickers"] = json.loads(rec["tickers"] or "[]")
            out.append(rec)
        return out

    def end_run(self) -> None:
        """Close the current run row; the connection stays open for the next stream."""
        if self.run_id is not None:
            self.conn.execute("UPDATE runs SET ended_at=? WHERE id=?", (time.time(), self.run_id))
            self.conn.commit()
            self.run_id = None

    async def close(self) -> None:
        self.end_run()
        self.conn.close()
