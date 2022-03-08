from olympicwordle.wordle import parse_scores, award_ceremony

wordles = (
    (
        "valid",
        (
            ("A", "Wordle 1 2/6"),
            ("BB", "Wordle 1 4/6"),
            ("CCC", "Wordle 1 5/6"),
            ("A", "Wordle 2 3/6"),
            ("BB", "Wordle 2 3/6"),
            ("CCC", "Wordle 2 6/6"),
            ("A", "Wordle 3 5/6"),
            ("BB", "Wordle 3 4/6"),
            ("CCC", "Wordle 3 2/6"),
        ),
        {"A": [1, 1, 0, 1, 0], "BB": [0, 1, 2, 0, 0], "CCC": [1, 0, 0, 1, 1]},
    ),
    (
        "invalid",
        (
            ("Oskar", "Wordle NaN 7/6"),
            ("Oskar", "Wordle 3 8/6"),
            ("Oskar", "Wordle 3 10"),
            ("Oskar", "Wordle 10"),
        ),
        {},
    ),
    (
        "multi",
        (
            ("A", "Wordle 4 5/6\nWordle 5 4/6"),
            ("B", "Wordle 4 4/6\nWordle 5 2/6"),
            ("C", "Wordle 4 2/6\nWordle 5 6/6"),
        ),
        {"A": [0, 0, 1, 1, 0], "B": [1, 0, 1, 0, 0], "C": [1, 0, 0, 0, 1]},
    ),
    (
        "updates",
        (
            ("A", "Wordle 1 2/6"),
            ("A", "Wordle 1 4/6"),
            ("A", "Wordle 1 5/6"),
        ),
        {"A": [0, 0, 0, 1, 0]},
    ),
)


def test_messages():
    for _, messages, awards in wordles:
        scores = parse_scores(messages)
        for score in scores:
            assert score["awards"] == awards[score["name"]]


def test_order():
    scores = parse_scores(wordles[0][1])
    assert "".join([s["name"] for s in scores]) == "ACCCBB"


def test_award_ceremony():
    scores = parse_scores(wordles[0][1])
    award_string = award_ceremony(scores)
    assert isinstance(award_string, str)
    print(award_string)


def test_emoji():
    msg = """
Wordle 262 3/6

⬛️⬛️⬛️⬛️🟨
⬛️⬛️⬛️🟨🟨
🟩⬛️🟩⬛️⬛️
🟩🟩🟩⬛️⬛️
🟩🟩🟩⬛️🟨
🟩🟩🟩🟩🟩
"""
    scores = parse_scores((("A", msg),))
    assert scores[0]["awards"] == [0, 1, 0, 0, 0]
