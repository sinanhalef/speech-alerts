"""Runtime configuration, loaded from environment variables and an optional .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _csv(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


@dataclass
class Settings:
    figure: str = os.getenv("FIGURE", "the president")

    deepgram_api_key: str = os.getenv("DEEPGRAM_API_KEY", "")
    deepgram_model: str = os.getenv("DEEPGRAM_MODEL", "nova-3")

    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "claude-haiku-4-5")
    llm_enabled: bool = os.getenv("LLM_ENABLED", "1") not in {"0", "false", "no"}
    llm_debounce_seconds: float = float(os.getenv("LLM_DEBOUNCE_SECONDS", "1.0"))
    llm_context_seconds: float = float(os.getenv("LLM_CONTEXT_SECONDS", "30"))
    llm_min_confidence: float = float(os.getenv("LLM_MIN_CONFIDENCE", "0.7"))

    # Speaker attribution: Deepgram streaming diarization + dominant-speaker gate.
    diarize: bool = os.getenv("DIARIZE", "1") not in {"0", "false", "no"}
    speaker_window_seconds: float = float(os.getenv("SPEAKER_WINDOW_SECONDS", "300"))
    speaker_min_words: int = int(os.getenv("SPEAKER_MIN_WORDS", "60"))

    sample_rate: int = 16000
    chunk_ms: int = 100

    cooldown_seconds: float = float(os.getenv("COOLDOWN_SECONDS", "600"))
    window_seconds: float = float(os.getenv("WINDOW_SECONDS", "90"))

    db_path: Path = Path(os.getenv("DB_PATH", str(PROJECT_ROOT / "data" / "alerts.sqlite3")))
    entities_path: Path = Path(
        os.getenv("ENTITIES_PATH", str(PROJECT_ROOT / "speechalerts" / "extract" / "entities.yaml"))
    )
    sec_tickers_path: Path = Path(
        os.getenv("SEC_TICKERS_PATH", str(PROJECT_ROOT / "data" / "entities" / "sec_tickers.json"))
    )

    web_host: str = os.getenv("WEB_HOST", "127.0.0.1")
    web_port: int = int(os.getenv("WEB_PORT", "8000"))

    # Discovery: channel /live pages to poll and title patterns that mark a relevant stream.
    watch_channels: list[str] = field(
        default_factory=lambda: _csv(
            "WATCH_CHANNELS",
            "https://www.youtube.com/@WhiteHouse/live,"
            "https://www.youtube.com/@cspan/live,"
            "https://www.youtube.com/@FoxNews/live",
        )
    )
    watch_title_patterns: list[str] = field(
        default_factory=lambda: _csv(
            "WATCH_TITLE_PATTERNS",
            r"president,cabinet meeting,oval office,white house",
        )
    )
    watch_poll_seconds: float = float(os.getenv("WATCH_POLL_SECONDS", "60"))
    watch_ignore_ended_hours: float = float(os.getenv("WATCH_IGNORE_ENDED_HOURS", "6"))
    watch_attach_retries: int = int(os.getenv("WATCH_ATTACH_RETRIES", "3"))

    # Live puller: how long without a new segment before asking YouTube whether the stream is
    # still live, and how many times a failed re-resolve is retried before giving up.
    live_stall_seconds: float = float(os.getenv("LIVE_STALL_SECONDS", "45"))
    live_resync_attempts: int = int(os.getenv("LIVE_RESYNC_ATTEMPTS", "5"))

    # Firebase sink: Firestore feed + FCM pushes (dry-run by default: validated, not delivered).
    firebase_enabled: bool = os.getenv("FIREBASE_ENABLED", "0") in {"1", "true", "yes"}
    firebase_project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    firebase_credentials: str = os.getenv("FIREBASE_CREDENTIALS", "")  # service-account JSON path; else ADC
    fcm_topic: str = os.getenv("FCM_TOPIC", "alerts")
    fcm_dry_run: bool = os.getenv("FCM_DRY_RUN", "1") not in {"0", "false", "no"}
    fcm_push_on_live: bool = os.getenv("FCM_PUSH_ON_LIVE", "1") not in {"0", "false", "no"}
    # Write final transcript segments to streams/{id}/segments (the hosted page shows them).
    firebase_transcripts: bool = os.getenv("FIREBASE_TRANSCRIPTS", "1") not in {"0", "false", "no"}

    ytdlp_cookies_from_browser: str = os.getenv("YTDLP_COOKIES_FROM_BROWSER", "")


settings = Settings()
