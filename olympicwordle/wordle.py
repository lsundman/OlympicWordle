from math import ceil
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
    max_len = sorted(map(lambda s: len(s["name"]), scores)).pop()
    max_wlen = sorted(map(lambda s: len(f"({len(s['wordles'])})"), scores)).pop()
    awards_header = " ".join(award_chars)
    return "\n".join(
        (
            "\N{TROPHY}".ljust(max_len + max_wlen + 4) + awards_header,
            "\n".join(
                [
                    "  ".join(
                        (
                            f"{s['name'].ljust(max_len)} ({len(s['wordles'])})",
                            "    ".join(str(s) for s in s["awards"]),
                        )
                    )
                    for s in scores
                ]
            ),
        )
    )
