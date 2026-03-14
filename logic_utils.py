import random


# FIXME: Normal and Hard ranges were swapped — Normal had the widest range and Hard had a narrower one,
# making Hard easier to guess than Normal. Corrected to match intended difficulty order.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        # FIX: was 1-100, corrected to 1-50
        return 1, 50
    if difficulty == "Hard":
        # FIX: was 1-50, corrected to 1-100
        return 1, 100
    return 1, 100


def generate_secret(low: int, high: int) -> int:
    """Pick a random secret number in [low, high] inclusive."""
    return random.randint(low, high)


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if not raw.strip():
        return False, None, "Please enter a number."
    try:
        return True, int(raw.strip()), None
    except ValueError:
        return False, None, f"'{raw}' is not a valid number."


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


# FIX: Implemented simple deterministic scoring — +1 for correct, -1 for wrong.
# Removed attempt_number since score no longer depends on it.
def update_score(current_score: int, outcome: str) -> int:
    """Update score based on outcome. +1 for Win, -1 for any wrong guess."""
    if outcome == "Win":
        return current_score + 1
    return current_score - 1
