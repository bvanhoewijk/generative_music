import json
from pprint import pprint
from numpy import arange
from simple_markov import *

# # https://github.com/generative-music/pieces-alex-bainter/blob/master/packages/piece-aisatsana/src/piece.js
BPM = 102
SECONDS_PER_MINUTE = 60
EIGHTH_NOTES_IN_BEAT = 2
EIGHTH_NOTE_INTERVAL_S = SECONDS_PER_MINUTE / (EIGHTH_NOTES_IN_BEAT * BPM)
SONG_LENGTH = 301
DELIMITER = ","

def phrases_from_json(jsonfile):
    with open(jsonfile, "r") as midi:
        data = midi.read()

    obj = json.loads(data)
    notes = obj["tracks"][1]["notes"]
    eigthNotes = list()

    for time in arange(0.0, SONG_LENGTH, EIGHTH_NOTE_INTERVAL_S):
        names = list(
            filter(
                lambda note: time <= note["time"]
                and note["time"] < time + EIGHTH_NOTE_INTERVAL_S,
                notes,
            )
        )
        names = list(map(lambda x: x["name"], names))
        names.sort()
        eigthNotes.append(DELIMITER.join(names))

    phrases = list()
    phraseLength = 32
    for i in range(0, len(eigthNotes), phraseLength):
        phrases.append(eigthNotes[i : i + phraseLength])

    # Add number:
    phrasesWithIndex = list(
        map(lambda phrase: [str(i + 1) + ":" + x for i, x in enumerate(phrase)], phrases)
    )
    # Add start and end 'tag'
    phrasesWithIndex = list(
        map(lambda phrase: ["start"] + phrase + ["end"], phrasesWithIndex)
    )
    return phrasesWithIndex

if __name__ == "__main__":
    phrasesWithIndex = phrases_from_json("data/instructions.json")

    transitions = calc_transitions(phrasesWithIndex)
    calc_possible_phrases(transitions)

    print(" ".join(phrasesWithIndex[0][1:]))

    new_phrases = list()
    for _ in range(1):
        print(" ".join(walk(transitions)))

  
    