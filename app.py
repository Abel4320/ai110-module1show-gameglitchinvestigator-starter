import streamlit as st
from logic_utils import (
    get_range_for_difficulty,
    generate_secret,
    parse_guess,
    check_guess,
    update_score,
)


# FIX: Shared helper used for first load, New Game, and difficulty change.
# Centralises round reset so the three callers can't drift out of sync.
# Score and input_counter are intentionally excluded — score persists across rounds,
# and input_counter is incremented here to rotate the widget key and clear the box.
def reset_round(low: int, high: int):
    st.session_state.secret = generate_secret(low, high)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.status = "playing"
    st.session_state.last_message = None
    st.session_state.input_counter += 1


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Score survives all resets — initialise it once and never touch it in reset_round.
if "score" not in st.session_state:
    st.session_state.score = 0

# input_counter must exist before reset_round is called (reset_round increments it).
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

# FIX: First load — call reset_round so secret, attempts, history, status, and
# last_message are all set consistently from one place.
if "secret" not in st.session_state:
    reset_round(low, high)

# FIX: Remember which difficulty was active so we can detect when it changes.
if "active_difficulty" not in st.session_state:
    st.session_state.active_difficulty = difficulty

# FIXME: Switching difficulty left the old secret, attempts, history, and hints intact.
# The secret could be outside the new range (e.g. secret=75 on Easy 1-20).
# FIX: Compare active_difficulty to the live sidebar value each run.
# If they differ, the user just switched — reset the round and rerun.
# Score is intentionally not reset.
if st.session_state.active_difficulty != difficulty:
    st.session_state.active_difficulty = difficulty
    reset_round(low, high)
    st.rerun()

st.subheader("Make a guess")

# FIX: Use the selected difficulty range instead of hardcoding 1 to 100.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret if st.session_state.get("show_hint", True) else "???")
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)



input_key = f"guess_input_{difficulty}_{st.session_state.input_counter}"
raw_guess = st.text_input(
    "Enter your guess:",
    key=input_key
)

# FIX: Render the saved hint here so it persists after st.rerun() clears the submit block.
if st.session_state.last_message:
    st.warning(st.session_state.last_message)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True, key="show_hint")


# FIX: New Game uses reset_round so it always generates a secret within the
# CURRENT difficulty range and clears all stale round state in one call.
if new_game:
    reset_round(low, high)
    st.success("New game started.")
    st.rerun()


if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()


if submit:
    # FIX: Validate input before counting attempts or adding to history.
    # This prevents empty/invalid guesses from corrupting the game state.
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        # FIX: Count every valid guess, including the first one.
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        # FIX: Save message to session state instead of rendering inline —
        # st.rerun() wipes any UI output rendered in the same run.
        st.session_state.last_message = message if show_hint else None

        # FIX: Score changes only here so it does not behave randomly.
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

        # FIX: Rotate the input key to clear the box without touching the widget directly.
        st.session_state.input_counter += 1
        st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")