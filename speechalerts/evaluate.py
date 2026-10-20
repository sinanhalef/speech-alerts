"""Golden-set evaluation: precision, recall and latency per stage.

Golden file (JSON):
{
  "source": "path/or/url/to/audio-or-video",      # optional if "transcript" is given
  "transcript": "eval/golden/foo.txt",            # optional: replay text instead of running STT
  "speed": 4,
  "expected": [ {"entity": "Intel", "tickers": ["INTC"], "t_audio": 42.0, "tolerance": 30} ]
}
Expected items match a CONFIRMED alert (or a HEADSUP when --no-llm) whose tickers intersect or
whose entity name matches, within `tolerance` seconds of t_audio.

  "not_expected": [ {"entity": "Oil", "t_audio": 301, "tolerance": 30} ]

Optional: alerts that must NOT fire (a reporter's question, a mis-heard name). A final alert
matching one is a false positive and is listed as `wrong:` in the summary.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass, field
from pathlib import Path

from speechalerts.models import Alert, AlertState


@dataclass
class EvalResult:
    name: str
    tp: int = 0
    fp: int = 0
    fn: int = 0
    matched: list[tuple[dict, Alert]] = field(default_factory=list)
    missed: list[dict] = field(default_factory=list)
    extra: list[Alert] = field(default_factory=list)
    wrong: list[tuple[dict, Alert]] = field(default_factory=list)
    latencies_ms: list[int] = field(default_factory=list)
    headsup_latencies_ms: list[int] = field(default_factory=list)

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 0.0


def _in_window(expected: dict, alert: Alert) -> bool:
    return abs(alert.t_audio - float(expected["t_audio"])) <= float(expected.get("tolerance", 30))


def _name_match(expected: dict, alert: Alert) -> bool:
    name = expected.get("entity", "").lower()
    return bool(name) and (name in alert.entity.lower() or alert.entity.lower() in name)


def _ticker_match(expected: dict, alert: Alert) -> bool:
    exp = {t.upper() for t in expected.get("tickers", [])}
    return bool(exp and exp & {t.upper() for t in alert.tickers})


def _matches(expected: dict, alert: Alert) -> bool:
    return _in_window(expected, alert) and (_name_match(expected, alert) or _ticker_match(expected, alert))


def score(
    name: str,
    expected: list[dict],
    alerts: list[Alert],
    *,
    final_state: AlertState,
    not_expected: list[dict] | None = None,
) -> EvalResult:
    res = EvalResult(name=name)
    # A heads-up's state is flipped to CONFIRMED when its child confirms; only alerts the model
    # itself produced (t_llm set) count as confirmed here.
    if final_state == AlertState.CONFIRMED:
        finals = [a for a in alerts if a.state == final_state and a.t_llm is not None]
    else:
        finals = [a for a in alerts if a.t_llm is None]
    used: set[str] = set()
    for exp in expected:
        # Prefer an alert naming the entity; fall back to one sharing a ticker (sector ETF alerts).
        hit = next((a for a in finals if a.id not in used and _in_window(exp, a) and _name_match(exp, a)), None)
        if hit is None:
            hit = next((a for a in finals if a.id not in used and _matches(exp, a)), None)
        if hit:
            used.add(hit.id)
            res.tp += 1
            res.matched.append((exp, hit))
        else:
            res.fn += 1
            res.missed.append(exp)
    for a in finals:
        if a.id not in used:
            res.fp += 1
            res.extra.append(a)
    for bad in not_expected or []:
        for a in finals:
            if _matches(bad, a):
                res.wrong.append((bad, a))
                if a.id in used:  # counted as a hit above; it is a miss-attribution, not a hit
                    res.tp -= 1
                    res.fp += 1
    res.latencies_ms = [a.latency_ms for a in finals]
    res.headsup_latencies_ms = [a.latency_ms for a in alerts if a.t_llm is None]
    return res


def summarize(results: list[EvalResult]) -> str:
    lines = [f"{'golden':28} {'TP':>3} {'FP':>3} {'FN':>3} {'prec':>6} {'rec':>6} "
             f"{'headsup p50':>12} {'p95':>6} {'confirm p50':>12} {'p95':>6}"]
    all_lat: list[int] = []
    all_hu: list[int] = []
    for r in results:
        all_lat += r.latencies_ms
        all_hu += r.headsup_latencies_ms
        lines.append(f"{r.name[:28]:28} {r.tp:3d} {r.fp:3d} {r.fn:3d} {r.precision:6.2f} {r.recall:6.2f} "
                     f"{_p50(r.headsup_latencies_ms):12.0f} {_p95(r.headsup_latencies_ms):6.0f} "
                     f"{_p50(r.latencies_ms):12.0f} {_p95(r.latencies_ms):6.0f}")
        for exp in r.missed:
            lines.append(f"    missed: {exp.get('entity')} {exp.get('tickers', [])} @ {exp.get('t_audio')}s")
        for a in r.extra:
            lines.append(f"    extra:  {a.entity} {a.tickers} @ {a.t_audio:.0f}s ({a.action}, conf {a.confidence:.2f})")
        for bad, a in r.wrong:
            lines.append(f"    wrong:  {a.entity} {a.tickers} @ {a.t_audio:.0f}s must not fire ({bad.get('reason', 'not_expected')})")
    tp = sum(r.tp for r in results); fp = sum(r.fp for r in results); fn = sum(r.fn for r in results)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    lines.append(f"{'TOTAL':28} {tp:3d} {fp:3d} {fn:3d} {prec:6.2f} {rec:6.2f} "
                 f"{_p50(all_hu):12.0f} {_p95(all_hu):6.0f} {_p50(all_lat):12.0f} {_p95(all_lat):6.0f}")
    return "\n".join(lines)


def _p50(values: list[int]) -> float:
    return float(statistics.median(values)) if values else 0.0


def _p95(values: list[int]) -> float:
    if not values:
        return 0.0
    vals = sorted(values)
    return float(vals[min(int(len(vals) * 0.95), len(vals) - 1)])


def golden_text_from_segments(rows: list[tuple[float, str, str | None]]) -> str:
    """Render stored segments as the replay format: t<TAB>[speaker<TAB>]text.

    `rows` are (t_audio_start, text, speaker_label); label "T" becomes speaker 0, "Q" speaker 1.
    Segments with no label are written without a speaker column.
    """
    lines = ["# Generated from a stored run: audio seconds, optional speaker id (0 = main speaker), text."]
    for t, text, label in rows:
        text = " ".join(text.split())
        if not text:
            continue
        spk = {"T": "0", "Q": "1"}.get(label or "")
        lines.append(f"{t:.1f}\t{spk}\t{text}" if spk else f"{t:.1f}\t{text}")
    return "\n".join(lines) + "\n"


def load_golden(path: Path) -> dict:
    data = json.loads(path.read_text())
    data.setdefault("name", path.stem)
    return data
