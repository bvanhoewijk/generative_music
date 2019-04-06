# Generative music
Playing with Markov chains. Heavily inspired by this fantastic medium post of Alex Bainter:

https://medium.com/@metalex9/generating-more-of-my-favorite-aphex-twin-track-cde9b7ecda3a


## simple_markov.py
Loads the 'small.txt' input file. Contents:

    start 1A 2F 3A 4F end
    start 1E 2C 3A 4C end

And generates a couple of phrases based on the input (it does not compute all possible phrases). Possible output:

    Total possible phrases: 4
    ['start', '1A', '2F', '3A', '4F', 'end']
    ['start', '1E', '2C', '3A', '4F', 'end']
    ['start', '1A', '2F', '3A', '4F', 'end']
    ['start', '1A', '2F', '3A', '4C', 'end']

## Meta info of ataisatsana:

    Track 0: Aphex Twin - aisatsana
    <meta message track_name name='Aphex Twin - aisatsana' time=0>
    <meta message copyright text='Notated by pianopeth 21.sep.2014' time=0>
    <meta message time_signature numerator=4 denominator=4 clocks_per_click=24 notated_32nd_notes_per_beat=8 time=0>
    <meta message key_signature key='C' time=0>
    <meta message set_tempo tempo=1176471 time=0>
    <meta message time_signature numerator=6 denominator=4 clocks_per_click=24 notated_32nd_notes_per_beat=8 time=241920>
    <meta message end_of_track time=0>
    Track 1: Piano
    <meta message track_name name='Piano' time=0>
    <meta message end_of_track time=0>

## TODO:
- check timing / duration of notes
- try this one: from mxm.midifile import MidiOutFile

