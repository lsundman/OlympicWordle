from olympicwordle.wordle_medals import parse_scores, award_ceremony


def test_medals():

    valid = (
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
        [
            ("A", [1, 1, 0, 1, 0]),
            ("CCC", [1, 0, 0, 1, 1]),
            ("BB", [0, 1, 2, 0, 0]),
        ],
    )

    invalid = (
        (
            ("Oskar", "Wordle NaN 7/6"),
            ("Oskar", "Wordle 3 8/6"),
            ("Oskar", "Wordle 3 10"),
            ("Oskar", "Wordle 10"),
        ),
        [],
    )

    multi = (
        (
            ("A", "Wordle 4 5/6\nWordle 5 4/6"),
            ("B", "Wordle 4 4/6\nWordle 5 2/6"),
            ("C", "Wordle 4 2/6\nWordle 5 6/6"),
        ),
        [("B", [1, 0, 1, 0, 0]), ("C", [1, 0, 0, 0, 1]), ("A", [0, 0, 1, 1, 0])],
    )

    updates = (
        (
            ("A", "Wordle 1 2/6"),
            ("A", "Wordle 1 4/6"),
            ("A", "Wordle 1 5/6"),
        ),
        [("A", [0, 0, 0, 1, 0])],
    )

    for msg, awards in (valid, invalid, multi, updates):
        assert parse_scores(msg) == awards

    wide = (
        (
            *(("A", f"Wordle {n} 4/6") for n in range(1, 120)),
            *(("BB", f"Wordle {n} 3/6") for n in range(1, 8)),
            *(("ABCDEFGHIJKL", f"Wordle {n} 5/6") for n in range(1, 4)),
        ),
        [
            ("A", [0, 0, 119, 0, 0]),
            ("BB", [0, 7, 0, 0, 0]),
            ("ABCDEFGHIJKL", [0, 0, 0, 3, 0]),
        ],
    )

    award_string = award_ceremony(wide[0])
    print(award_string)

    assert isinstance(award_string, str)
