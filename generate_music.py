import sys
from midiutil import MIDIFile
from pprint import pprint
import time
import math
import pygame
import pygame.mixer
import base64
from numpy import arange
from collections import defaultdict
import random
import json

BPM = 102
SECONDS_PER_MINUTE = 60
EIGHTH_NOTES_IN_BEAT = 2
EIGHTH_NOTE_INTERVAL_S = SECONDS_PER_MINUTE / (EIGHTH_NOTES_IN_BEAT * BPM)
SONG_LENGTH = 301
DELIMITER = ","


def phrases_from_json(jsonfile):
    """Parse the JSON file and create phrases"""
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
        names = list(
            map(
                lambda x: x["name"]
                + ":"
                + str(round(x["duration"], 2))
                + ":"
                + str(round(x["velocity"], 2)),
                names,
            )
        )
        names.sort()
        eigthNotes.append(DELIMITER.join(names))

    phrases = list()
    phraseLength = 32
    for i in range(0, len(eigthNotes), phraseLength):
        phrases.append(eigthNotes[i : i + phraseLength])

    # Add number:
    phrasesWithIndex = list(
        map(
            lambda phrase: [str(i + 1) + "," + x for i, x in enumerate(phrase)], phrases
        )
    )

    # Add start and end 'tag'
    phrasesWithIndex = list(
        map(lambda phrase: ["start"] + phrase + ["end"], phrasesWithIndex)
    )

    return phrasesWithIndex


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
    return chain[1 : len(chain) - 1]


def calc_possible_phrases(transitions):
    """Calculate the amount of possible phrases."""
    total = 1
    for item in transitions:
        total *= len(set(transitions[item]))
    print("Total possible phrases: %s" % total)


def noteName(noteNumber):
    """Notenumber to Notename"""
    noteNumber -= 21
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    octave = math.ceil(noteNumber / 12)
    name = notes[noteNumber % 12]
    return str(name) + str(octave)


def noteNumber(noteName):
    """Notename to Notenumber"""
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    note = noteName[0]
    octave = int(noteName[1]) - 1

    index = notes.index(note)

    return index + octave * 12 + 21


def play_song(music_file):
    """Play a midi song"""
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    try:
        # use the midi file object from memory
        pygame.mixer.music.load(music_file)
        clock = pygame.time.Clock()
        pygame.mixer.music.play()
        # check if playback has finished
        while pygame.mixer.music.get_busy():
            clock.tick(30)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit


def create_song(music_file, phrases):
    """Create a song using the calculated phrases and a file name"""
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 0.58  # 0.58  # In beats
    tempo = 51  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)
    MyMIDI.addProgramChange(0, 0, 0, 0)
    phrasecount = 0

    for phrase in phrases:
        for notes in phrase:
            result = notes.split(",")
            index = result[0]
            note_list = result[1:]
            for note in note_list:
                if note:
                    note_name, duration, velocity = note.split(":")
                    time = (int(index) * 0.31) + (32 * 0.31 * phrasecount)
                    MyMIDI.addNote(
                        track,
                        channel,
                        int(noteNumber(note_name)),
                        time,
                        float(duration),
                        int(volume * float(velocity)),
                    )
        phrasecount += 1

    with open(music_file, "wb") as output_file:
        MyMIDI.writeFile(output_file)


def play_original():
    music_file = "new_song.mid"
    phrasesWithIndex = phrases_from_json("data/instructions.json")

    new_phrases = list()
    for phrase in phrasesWithIndex:
        new_phrases.append(phrase[1 : len(phrase) - 1])

    create_song(music_file, new_phrases)

    play_song(music_file)


if __name__ == "__main__":
    play_original()
    # sys.exit()
    music_file = "new_song.mid"
    phrasesWithIndex = phrases_from_json("data/instructions.json")

    transitions = calc_transitions(phrasesWithIndex)
    pprint(transitions)
    calc_possible_phrases(transitions)

    new_phrases = list()
    for _ in range(20):
        new_phrase = walk(transitions)
        new_phrases.append(new_phrase)

    create_song(music_file, new_phrases)

    play_song(music_file)

