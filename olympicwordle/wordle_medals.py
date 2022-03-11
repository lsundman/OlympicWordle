from collections import namedtuple

from olympicwordle.wordle import parse_messages

award_template = [0, 0, 0, 0, 0]
award_chars = (
    "\N{GEM STONE}",
    "\N{FIRST PLACE MEDAL}",
    "\N{SECOND PLACE MEDAL}",
    "\N{THIRD PLACE MEDAL}",
    "\N{ROCK}",
)
award_mapping = {1: 0, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4}

Medals = namedtuple("Medals", "name medals")


def parse_scores(messages):
    scores = []
    for name, wordles in parse_messages(messages):
        awards = award_template.copy()
        for _, guesses in wordles:
            awards[award_mapping[guesses]] += 1

        scores.append(Medals(name, awards))

    scores.sort(key=lambda t: t.medals, reverse=True)
    return scores


def award_ceremony(messages):
    scores = parse_scores(messages)

    m_amount = lambda s: f"({sum(s.medals)})"
    max_name = max(map(lambda s: len(s.name), scores))
    max_amount = max(map(lambda s: len(m_amount(s)), scores))
    max_cell = max((max([len(str(m)) for m in s.medals]) for s in scores))

    return "\n".join(
        (
            "\n".join(
                [
                    "\n".join(
                        (
                            f"{i}. {s.name} ({sum(s.medals)})",
                            " ".join(
                                f"{award_chars[i]} {n}" for i, n in enumerate(s.medals)
                            ),
                            "──────────────────────",
                        )
                    )
                    for i, s in enumerate(scores, start=1)
                ]
            ),
        )
    )
