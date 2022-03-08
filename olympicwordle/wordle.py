from math import ceil
import re

regex = re.compile(r"Wordle (?P<wordle>\d{1,3}) (?P<guesses>[1-6])\/6")

award_template = [0, 0, 0, 0]
award_chars = (
    "\N{GEM STONE}",
    "\N{FIRST PLACE MEDAL}",
    "\N{SECOND PLACE MEDAL}",
    "\N{THIRD PLACE MEDAL}",
)
award_mapping = {1: 0, 2: 0, 3: 1, 4: 2, 5: 3}


def parse_scores(messages):
    user_wordles = {}
    for user, message in messages:
        for match in regex.finditer(message):
            wordle = int(match.groupdict()["wordle"])
            guesses = int(match.groupdict()["guesses"])

            user_wordles.setdefault(user, {})
            user_wordles[user][wordle] = award_mapping.get(guesses, None)

    result = {}
    for user, ws in user_wordles.items():
        awards = award_template.copy()
        for _, idx in ws.items():
            if idx is not None:
                awards[idx] += 1

        result[user] = awards

    scores = dict(sorted(result.items(), key=lambda t: t[1], reverse=True))

    return scores


def award_ceremony(scores):
    return "\n".join(
        (
            "\t".join(("**Namn**", " ".join(award_chars))),
            "\n".join(
                [
                    "\t".join((n, " ".join((f"{v}" for v in vals))))
                    for n, vals in scores.items()
                ]
            ),
        )
    )
