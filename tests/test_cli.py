import pytest

from speechalerts.cli import build_parser, parse_clock


def test_parse_clock_formats():
    assert parse_clock("12") == 720
    assert parse_clock("12.5") == 750
    assert parse_clock("12:30") == 750
    assert parse_clock("1:02:30") == 3750
    with pytest.raises(Exception):
        parse_clock("1:2:3:4")


def test_replay_accepts_from_to():
    args = build_parser().parse_args(["replay", "x.mp4", "--from", "5", "--to", "7:30", "--speed", "4"])
    assert args.start == "5" and args.end == "7:30" and args.speed == 4.0
