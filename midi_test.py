#!/usr/bin/env python

import midiutil
from midiutil import MIDIFile
from mido import MidiFile
from pprint import pprint
import time
import math
import pygame
import pygame.mixer
import base64

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


def create_song(music_file):
    degrees = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 0.58  # In beats
    tempo = 51  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)
    
    phrase = "1:E3 2: 3:G3 4: 5:C3 6: 7:C4 8: 9: 10: 11: 12: 13: 14: 15: 16: 17: 18: 19: 20: 21: 22: 23: 24: 25: 26: 27: 28: 29: 30: 31: 32:"
    # phrase = "1:C5,E3,E4 2:B4 3:A4,E4,G3 4:B4 5:C3,C5,D4 6: 7:C4,E3,G6 8: 9:B3,D3 10: 11: 12: 13:E4 14: 15: 16: 17:E4 18: 19: 20: 21: 22: 23: 24: 25: 26: 27: 28: 29: 30: 31: 32:"
    notes = phrase.split(" ")
    i = 0
    for note in notes:
        index, notenames = note.split(":")
        notenames = notenames.split(",")
        for n in notenames:
            if n:
                MyMIDI.addNote(track, channel, int(noteNumber(n)), int(index)*0.31, duration, volume)
                print("MyMIDI.addNote(%s, %s, %s, %s, %s, %s)" % (track, channel, int(noteNumber(n)), int(index)*0.31, duration, volume))
    
    with open(music_file, "wb") as output_file:
        MyMIDI.writeFile(output_file)


# def create_song(music_file):
#     degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
#     track    = 0
#     channel  = 0
#     time     = 0       # In beats
#     duration = 0.58    # In beats
#     tempo    = 51      # In BPM
#     volume   = 100     # 0-127, as per the MIDI standard

#     MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
#                         # automatically)
#     MyMIDI.addTempo(track, time, tempo)

#     MyMIDI.addNote(track, channel, degrees[0], 0, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[1], 1, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[2], 2, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[3], 3, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[4], 4, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[5], 5, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[6], 6, duration, volume)
#     MyMIDI.addNote(track, channel, degrees[7], 7, duration, volume)

#     with open(music_file, "wb") as output_file:
#         MyMIDI.writeFile(output_file)

if __name__ == "__main__":
    # print(noteNumber("E4"))
    music_file = "new_song.mid"

    create_song(music_file)

    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
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

