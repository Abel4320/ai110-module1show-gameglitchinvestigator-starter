import sys
import os

# Make the project root importable regardless of where pytest is invoked from.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ---------------------------------------------------------------------------
# check_guess(guess, secret) -> (outcome, message)
# ---------------------------------------------------------------------------

def test_check_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_check_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_win():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# parse_guess(raw) -> (ok, value, error)
# ---------------------------------------------------------------------------

def test_parse_guess_valid():
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_guess_empty():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_whitespace():
    ok, value, _ = parse_guess("   ")
    assert ok is False
    assert value is None

def test_parse_guess_non_numeric():
    ok, value, _ = parse_guess("abc")
    assert ok is False
    assert value is None

def test_parse_guess_float_string():
    # "3.14" cannot be parsed as int
    ok, value, _ = parse_guess("3.14")
    assert ok is False
    assert value is None


# ---------------------------------------------------------------------------
# get_range_for_difficulty(difficulty) -> (low, high)
# ---------------------------------------------------------------------------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 100)


# ---------------------------------------------------------------------------
# update_score(current_score, outcome) -> int
# ---------------------------------------------------------------------------

def test_update_score_win():
    assert update_score(5, "Win") == 6

def test_update_score_wrong():
    assert update_score(5, "Too High") == 4

def test_update_score_too_low():
    assert update_score(5, "Too Low") == 4

def test_update_score_from_zero():
    # Score can go negative
    assert update_score(0, "Too High") == -1
