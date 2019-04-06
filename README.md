# Generative music
Playing with Markov chains. Heavily inspired by this fantastic medium post of Alex Bainter:

https://medium.com/@metalex9/generating-more-of-my-favorite-aphex-twin-track-cde9b7ecda3a


## simple_markov.py
Loads the 'small.txt' input file. Contents:

    start 1A 2F 3A 4F end
    start 1E 2C 3A 4C end

And generates a couple of new phrases based on the input. Possible output:

    Total possible phrases: 4
    ['start', '1A', '2F', '3A', '4F', 'end']
    ['start', '1E', '2C', '3A', '4F', 'end']
    ['start', '1A', '2F', '3A', '4F', 'end']
    ['start', '1A', '2F', '3A', '4C', 'end']