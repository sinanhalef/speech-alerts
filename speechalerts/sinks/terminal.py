"""Terminal sink using rich: one line per alert, dim rolling transcript."""

from __future__ import annotations

from datetime import datetime

from rich.console import Console
from rich.text import Text

from speechalerts.models import Alert, AlertState, TranscriptSegment

_STYLE = {
    AlertState.HEADSUP: "bold yellow",
    AlertState.CONFIRMED: "bold green",
    AlertState.RETRACTED: "dim red",
}
_STANCE = {"positive": "green", "negative": "red", "neutral": "white"}


class TerminalSink:
    def __init__(self, *, show_transcript: bool = True, show_interim: bool = False) -> None:
        self.console = Console(highlight=False)
        self.show_transcript = show_transcript
        self.show_interim = show_interim

    async def alert(self, alert: Alert) -> None:
        ts = datetime.fromtimestamp(alert.t_alert).strftime("%H:%M:%S")
        line = Text()
        line.append(f"{ts} ", style="dim")
        line.append(f"[{alert.state.value.upper():9}] ", style=_STYLE[alert.state])
        line.append(f"{alert.entity} ", style="bold")
        if alert.tickers:
            line.append(" ".join(alert.tickers) + " ", style="cyan")
        if alert.state == AlertState.CONFIRMED:
            line.append(f"{alert.stance}/{alert.action} ", style=_STANCE.get(alert.stance, "white"))
            line.append(f"conf={alert.confidence:.2f} ", style="dim")
        if alert.word_confidence < 0.9:
            line.append(f"stt={alert.word_confidence:.2f} ", style="dim yellow")
        line.append(f"+{alert.latency_ms} ms", style="magenta")
        self.console.print(line)
        detail = alert.summary if alert.state == AlertState.CONFIRMED else alert.quote
        if detail:
            self.console.print(Text(f"    {detail}", style="italic" if alert.state == AlertState.CONFIRMED else "dim"))
        if alert.state == AlertState.CONFIRMED and alert.quote:
            self.console.print(Text(f'    "{alert.quote}"', style="dim"))

    async def segment(self, seg: TranscriptSegment) -> None:
        if not self.show_transcript:
            return
        tag = f"{seg.speaker_label:1}" if seg.speaker_label else " "
        if seg.is_final:
            style = "dim" if seg.speaker_label != "Q" else "dim cyan"
            self.console.print(Text(f"{tag} {seg.t_audio_start:8.1f}s  {seg.text}", style=style))
        elif self.show_interim:
            self.console.print(Text(f"{tag} {seg.t_audio_start:8.1f}s ~ {seg.text}", style="dim italic"))

    async def close(self) -> None:
        return None
