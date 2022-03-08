from olympicwordle.wordle import parse_scores, award_ceremony

wordles = {
    "valid": (
        ("A", "Wordle 1 2/6"),
        ("B", "Wordle 1 4/6"),
        ("C", "Wordle 1 5/6"),
        ("A", "Wordle 2 3/6"),
        ("B", "Wordle 2 3/6"),
        ("C", "Wordle 2 6/6"),
        ("A", "Wordle 3 5/6"),
        ("B", "Wordle 3 4/6"),
        ("C", "Wordle 3 2/6"),
    ),
    "invalid": (
        ("Oskar", "Wordle NaN 7/6"),
        ("Oskar", "Wordle 3 8/6"),
        ("Oskar", "Wordle 3 10"),
        ("Oskar", "Wordle 10"),
    ),
    "multi": (
        ("A", "Wordle 4 5/6\nWordle 5 4/6"),
        ("B", "Wordle 4 4/6\nWordle 5 2/6"),
        ("C", "Wordle 4 2/6\nWordle 5 6/6"),
    ),
    "updates": (
        ("A", "Wordle 1 2/6"),
        ("A", "Wordle 1 4/6"),
        ("A", "Wordle 1 5/6"),
    ),
}


def test_valid():
    result = parse_scores(wordles["valid"])
    assert result["A"] == [1, 1, 0, 1]
    assert result["B"] == [0, 1, 2, 0]
    assert result["C"] == [1, 0, 0, 1]


def test_invalid():
    result = parse_scores(wordles["invalid"])

    assert not result


def test_multiple():
    result = parse_scores(wordles["multi"])

    assert result["A"] == [0, 0, 1, 1]
    assert result["B"] == [1, 0, 1, 0]
    assert result["C"] == [1, 0, 0, 0]


def test_order():
    scores = parse_scores(wordles["valid"])
    names = [n for n, s in scores.items()]
    assert names.index("A") == 0
    assert names.index("C") == 1
    assert names.index("B") == 2


def test_updates():
    scores = parse_scores(wordles["updates"])
    assert scores["A"] == [0, 0, 0, 1]


def test_award_ceremony():
    scores = parse_scores(wordles["valid"])
    award_ceremony(scores)


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
    assert scores["A"] == [0, 1, 0, 0]
