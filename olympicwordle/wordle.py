import re

regex = re.compile(r"Wordle (?P<wordle>\d{1,3}) (?P<guesses>[1-6])\/6")

award_template = [0, 0, 0, 0, 0]
award_chars = (
    "\N{GEM STONE}",
    "\N{FIRST PLACE MEDAL}",
    "\N{SECOND PLACE MEDAL}",
    "\N{THIRD PLACE MEDAL}",
    "\N{ROCK}",
)
award_mapping = {1: 0, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4}


def parse_scores(messages):
    user_wordles = {}
    for user, message in messages:
        for match in regex.finditer(message):
            wordle = int(match.groupdict()["wordle"])
            guesses = int(match.groupdict()["guesses"])

            user_wordles.setdefault(user, {})
            user_wordles[user][wordle] = award_mapping.get(guesses, None)

    result = []
    for user, ws in user_wordles.items():
        awards = award_template.copy()
        for _, idx in ws.items():
            if idx is not None:
                awards[idx] += 1

        result.append({"name": user, "wordles": list(ws.keys()), "awards": awards})

    scores = sorted(result, key=lambda res: res["awards"], reverse=True)
    return scores


def award_ceremony(scores):
    max_len = max(map(lambda s: len(s["name"]), scores))
    max_wlen = max(map(lambda s: len(f"({sum(s['awards'])})"), scores))
    max_alen = max(
        (
            *[max([len(str(a)) for a in s["awards"]]) for s in scores],
            max(len(c) for c in award_chars),
        )
    )
    return "\n".join(
        (
            "```",
            " ".join(
                (
                    "\N{TROPHY}".ljust(max_len + max_wlen),
                    " ".join(s.ljust(max_alen - 1) for s in award_chars),
                )
            ),
            "\n".join(
                [
                    "  ".join(
                        (
                            f"{s['name'].ljust(max_len)} ({sum(s['awards'])})",
                            " ".join(str(s).ljust(max_alen) for s in s["awards"]),
                        )
                    )
                    for s in scores
                ]
            ),
            "```",
        )
    )
