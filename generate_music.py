import midiutil
from midiutil import MIDIFile
from mido import MidiFile
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
        map(
            lambda phrase: [str(i + 1) + ":" + x for i, x in enumerate(phrase)], phrases
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
    noteNumber -= 21
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    octave = math.ceil(noteNumber / 12)
    name = notes[noteNumber % 12]
    return str(name) + str(octave)


def noteNumber(noteName):
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    note = noteName[0]
    octave = int(noteName[1]) - 1

    index = notes.index(note)

    return index + octave * 12 + 21


def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    pygame.mixer.music.load(music_file)
    clock = pygame.time.Clock()
    pygame.mixer.music.play()
    # check if playback has finished
    while pygame.mixer.music.get_busy():
        clock.tick(30)


def play_song(music_file):
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
        play_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit

def create_song(music_file, phrases):
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 0.58  # In beats
    tempo = 51  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)

    phrasecount = 0
    for phrase in phrases:
        for notes in phrase:
            index, notenames = notes.split(":")
            notenames = notenames.split(",")
            for n in notenames:
                if n:
                    time = (int(index) * 0.31) + (32 * 0.31 * phrasecount)
                    MyMIDI.addNote(
                        track, channel, int(noteNumber(n)), time, duration, volume
                    )
                    print(
                        "MyMIDI.addNote(%s, %s, %s, %s, %s, %s)"
                        % (track, channel, int(noteNumber(n)), time, duration, volume)
                    )
        phrasecount += 1

    with open(music_file, "wb") as output_file:
        MyMIDI.writeFile(output_file)



if __name__ == "__main__":
    # print(noteNumber("E4"))
    music_file = "new_song.mid"

    phrasesWithIndex = phrases_from_json("data/instructions.json")

    transitions = calc_transitions(phrasesWithIndex)
    calc_possible_phrases(transitions)

    new_phrases = list()
    for _ in range(50):
        new_phrases.append(walk(transitions))

    print(new_phrases)
    create_song(music_file, new_phrases)

    play_song(music_file)

