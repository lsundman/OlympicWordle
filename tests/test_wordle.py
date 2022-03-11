from olympicwordle.wordle import parse_messages


def test_parser():
    parsed = parse_messages(
        [
            *(("A", f"Wordle {n} 2/6") for n in range(0, 6)),
            *(("B", f"Wordle {n} 4/6") for n in range(0, 6)),
            *(("C", f"Wordle {n} 6/6") for n in range(0, 6)),
        ]
    )

    for name, ws in parsed:
        assert len(ws) == 6
        if name == "A":
            assert ws[0].guesses == 2
        elif name == "B":
            assert ws[0].guesses == 4
        elif name == "C":
            assert ws[0].guesses == 6

    emoji_msg = """
Wordle 262 3/6

⬛️⬛️⬛️⬛️🟨
⬛️⬛️⬛️🟨🟨
🟩⬛️🟩⬛️⬛️
🟩🟩🟩⬛️⬛️
🟩🟩🟩⬛️🟨
🟩🟩🟩🟩🟩
"""
    parsed = parse_messages((("A", emoji_msg),))
    assert parsed[0].name == "A"
    assert parsed[0].result == ((262, 3),)
