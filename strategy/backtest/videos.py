"""videos.yaml loader."""

from __future__ import annotations

from pathlib import Path

import yaml

from backtest.models import VideoSpec

STRATEGY_ROOT = Path(__file__).resolve().parent.parent
DATA = STRATEGY_ROOT / "data"
VIDEOS_YAML = STRATEGY_ROOT / "videos.yaml"


def load_videos(path: Path | None = None, *, only: list[str] | None = None, include_skipped: bool = False) -> list[VideoSpec]:
    raw = yaml.safe_load((path or VIDEOS_YAML).read_text()) or {}
    specs = [VideoSpec.model_validate(item) for item in raw.get("videos", [])]
    if only:
        wanted = set(only)
        specs = [s for s in specs if s.id in wanted]
        missing = wanted - {s.id for s in specs}
        if missing:
            specs += [VideoSpec(id=i, group="other") for i in sorted(missing)]
    if not include_skipped:
        specs = [s for s in specs if not s.skip]
    return specs
