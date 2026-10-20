import pytest

from speechalerts.extract.dictionary import Dictionary
from speechalerts.models import TranscriptSegment


@pytest.fixture(scope="session")
def dictionary() -> Dictionary:
    return Dictionary.load(sec_path=None)


def seg(text: str, start: float = 10.0, end: float = 14.0, final: bool = True) -> TranscriptSegment:
    return TranscriptSegment(text=text, t_audio_start=start, t_audio_end=end, t_wall=1000.0, is_final=final)


@pytest.fixture
def make_seg():
    return seg
