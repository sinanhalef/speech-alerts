"""Copy a run's final transcript segments from the local SQLite log into Firestore
`streams/{video_id}/segments/{t_wall_ms}` (same shape as FirebaseSink.segment writes).

    uv run python scripts/backfill_transcript.py --run 48 --stream 2uOpDXhd990
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from speechalerts.config import settings  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=int, required=True, help="runs.id in data/alerts.sqlite3")
    ap.add_argument("--stream", required=True, help="YouTube video id (streams/{id})")
    ap.add_argument("--db", default=str(ROOT / "data" / "alerts.sqlite3"))
    ap.add_argument("--wall-from-release", type=float, default=None,
                    help="for a replayed recording: stream release_timestamp; t_wall = release + t_audio_start")
    ap.add_argument("--until-audio", type=float, default=None, help="skip segments after this audio position (s)")
    args = ap.parse_args()

    if settings.firebase_credentials and not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.firebase_credentials
    import firebase_admin
    from firebase_admin import firestore

    firebase_admin.initialize_app(options={"projectId": settings.firebase_project_id} if settings.firebase_project_id else None)
    db = firestore.client()

    conn = sqlite3.connect(args.db)
    rows = conn.execute(
        "SELECT t_audio_start, t_audio_end, t_wall, confidence, text, speaker_label FROM segments "
        "WHERE run_id = ? AND trim(text) != '' ORDER BY t_wall",
        (args.run,),
    ).fetchall()
    col = db.collection("streams").document(args.stream).collection("segments")
    batch, n = db.batch(), 0
    for t0, t1, t_wall, conf, text, label in rows:
        if args.until_audio is not None and t0 > args.until_audio:
            continue
        if args.wall_from_release is not None:
            t_wall = args.wall_from_release + t0
        batch.set(col.document(f"{int(t_wall * 1000):016d}"), {
            "text": text, "t_audio_start": t0, "t_audio_end": t1, "t_wall": t_wall,
            "confidence": conf, "speaker_label": label or "",
        })
        n += 1
        if n % 400 == 0:
            batch.commit(); batch = db.batch()
    batch.commit()
    print(f"wrote {n} segments to streams/{args.stream}/segments")


if __name__ == "__main__":
    main()
