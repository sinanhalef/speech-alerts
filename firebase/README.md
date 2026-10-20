# Firebase project config

Project: `your-firebase-project` (console: https://console.firebase.google.com/project/your-firebase-project).

- `firestore.rules`: clients read-only; the backend writes via the Admin SDK.
- Deploy rules: `cd firebase && firebase deploy --only firestore:rules`.
- Backend credentials: `secrets/your-firebase-project-sa.json` (gitignored), path in `.env` as
  `FIREBASE_CREDENTIALS`.

Collections written by `speechalerts/sinks/firebase.py`:

| Path | Content |
|---|---|
| `alerts/{alert_id}` | one document per alert emit (`Alert.to_dict()` + `stream_id`, `stream_title`, `created_at`); confirmed/retracted children also merge `state`, `resolved_by`, `resolved_at` into their heads-up parent |
| `streams/{video_id}` | one per live broadcast: `title`, `watch_url`, `state` (live/ended), `started_at`, `ended_at`, `end_reason`, counts |
| `status/current` | the daemon's state: `state` (polling/attaching/listening/ended), `title`, `video_id`, `last_poll`, `channels` |

Pushes go to the FCM topic `alerts` (`FCM_TOPIC`). With `FCM_DRY_RUN=1` they are validated by FCM
but not delivered, and the backend logs `would push ...`.

## Hosting (the terminal-style feed page)

- URL: https://<your-site>.web.app (site `your-firebase-project`, web app "Speech Alerts Web").
- Files: `public/index.html`, `public/app.css`, `public/app.js`. Firebase config comes from the
  Hosting reserved URL `/__/firebase/init.js`, so nothing is embedded; the page uses the compat
  SDK (`/__/firebase/10.14.1/...`) and Firestore `onSnapshot` on `status/current`, `events`
  (ordered by `starts_at`) and `alerts` (ordered by `created_at`, last 400).
- Deploy: `cd firebase && firebase deploy --only hosting`.
- Times are shown in the viewer's zone (`Intl.DateTimeFormat().resolvedOptions().timeZone`);
  `?tz=Europe/Berlin` overrides it. Events also show the venue time from their `tz`.
- Schedule: `events/{id}` documents come from `data/schedule.yaml` via
  `uv run python scripts/push_schedule.py` (`--prune` deletes events removed from the file).
  Fields: `title`, `kind`, `venue`, `city`, `tz`, `starts_at`, optional `doors_at`, `source_url`.
- "quotes" shows the verbatim words that raised each alert (`Alert.quote`).
- The right pane is the live transcript: `streams/{video_id}/segments/{t_wall_ms}` (final
  segments only, written by `FirebaseSink.segment` while `FIREBASE_TRANSCRIPTS=1`; keyed by
  wall-clock so re-attaches to the same video stay ordered). It follows the stream the listener
  is on, or whichever stream is picked under "quotes". Backfill a past run from SQLite with
  `uv run python scripts/backfill_transcript.py --run <id> --stream <video_id>`.
  Rules are world-readable, so treat this as a private dev feed: Stage 2 must not ship it.
