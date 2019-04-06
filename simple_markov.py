#!/usr/bin/env python3
# https://medium.com/@metalex9/generating-more-of-my-favorite-aphex-twin-track-cde9b7ecda3a
from collections import defaultdict
from pprint import pprint
import random


def load_song_txt(filename):
    """Load the 'song' into a list of lists. Each list has a list of notes."""
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip().split(" ") for x in content]
    return content


def calc_transitions(content):
    """Calculate the possible transitions based on the input phrases"""
    transitions = defaultdict(list)
    for phrase in content:
        for i in range(len(phrase) - 1):
            transitions[phrase[i]].append(phrase[i + 1])
    return transitions


def walk(transitions):
    """Walk the chain and chose a random option when it comes to that"""
    item = "start"
    chain = list()
    chain.append(item)
    while item != "end":
        options = transitions[item]
        if len(options) > 1:
            item = options[random.randint(0, len(options) - 1)]
        elif len(options) == 1:
            item = options[0]
        chain.append(item)
    return chain[1:len(chain)-1]


def calc_possible_phrases(transitions):
    """Calculate the amount of possible phrases."""
    total = 1
    for item in transitions:
        total *= len(set(transitions[item]))
    print("Total possible phrases: %s" % total)


if __name__ == "__main__":
    content = load_song_txt("data/small.txt")
    transitions = calc_transitions(content)
    calc_possible_phrases(transitions)

    print(walk(transitions))
    print(walk(transitions))
    print(walk(transitions))
    print(walk(transitions))

    # Possible output:
    # Total possible phrases: 4
    # ['start', '1A', '2F', '3A', '4F', 'end']
    # ['start', '1E', '2C', '3A', '4F', 'end']
    # ['start', '1A', '2F', '3A', '4F', 'end']
    # ['start', '1A', '2F', '3A', '4C', 'end']
