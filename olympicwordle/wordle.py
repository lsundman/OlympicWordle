from collections import defaultdict, namedtuple
import re

regex = re.compile(r"Wordle (?P<wordle>\d{1,3}) (?P<guesses>[1-6])\/6")

Player = namedtuple("Player", "name result")
Result = namedtuple("Result", "wordle guesses")


def parse_messages(messages):
    result = defaultdict(dict)
    for user, message in messages:
        for match in regex.finditer(message):
            groups = match.groupdict()
            result[user][groups["wordle"]] = groups["guesses"]

    return [
        Player(name, tuple(Result(int(w), int(g)) for w, g in wordles.items()))
        for name, wordles in result.items()
    ]
