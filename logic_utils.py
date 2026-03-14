def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


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
