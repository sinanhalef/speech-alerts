"""Upsert data/schedule.yaml into Firestore `events/{id}` (read by the hosted page).

    uv run python scripts/push_schedule.py            # upsert every event in the file
    uv run python scripts/push_schedule.py --prune    # also delete events no longer in the file
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from speechalerts.config import settings  # noqa: E402

REQUIRED = ("id", "title", "kind", "venue", "city", "tz", "starts_at")


def load_events(path: Path) -> list[dict]:
    raw = yaml.safe_load(path.read_text()) or {}
    events = []
    for ev in raw.get("events", []):
        missing = [k for k in REQUIRED if k not in ev]
        if missing:
            raise SystemExit(f"event {ev.get('id', '?')}: missing {missing}")
        doc = dict(ev)
        for key in ("starts_at", "doors_at", "ends_at"):
            if key in doc:
                dt = datetime.fromisoformat(str(doc[key]))
                if dt.tzinfo is None:
                    raise SystemExit(f"event {ev['id']}: {key} needs a UTC offset")
                doc[key] = dt
        doc["figure"] = doc.get("figure", settings.figure)
        events.append(doc)
    return events


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(ROOT / "data" / "schedule.yaml"))
    ap.add_argument("--prune", action="store_true", help="delete events not present in the file")
    args = ap.parse_args()

    if settings.firebase_credentials and not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.firebase_credentials
    import firebase_admin
    from firebase_admin import firestore

    firebase_admin.initialize_app(options={"projectId": settings.firebase_project_id} if settings.firebase_project_id else None)
    db = firebase_admin.firestore.client() if hasattr(firebase_admin, "firestore") else firestore.client()

    events = load_events(Path(args.file))
    col = db.collection("events")
    batch = db.batch()
    for ev in events:
        batch.set(col.document(ev["id"]), {**ev, "updated_at": firestore.SERVER_TIMESTAMP}, merge=True)
    batch.commit()
    print(f"upserted {len(events)} events")

    if args.prune:
        keep = {ev["id"] for ev in events}
        stale = [d.reference for d in col.stream() if d.id not in keep]
        for ref in stale:
            ref.delete()
        print(f"deleted {len(stale)} stale events")


if __name__ == "__main__":
    main()
