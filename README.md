A respository holding all of the small tools I've made.

Listing
=========

Delta
-------
Written in Java. Given a txt file with a list of items, Delta will
choose one for you using a PRNG. Each item is denoted with a '>>' or a
'<<'. When choosing, Delta will ignore all items prefixed with
'<<'. This is useful if you don't want any item to be chosen more than
once. Originally written to decrease the embarassing amount of time my
indecisive college roommate and I spent deciding what to do.

plc
---
Written in Python. Given one or more directories as input, it will
find all audio files and create Media Player Classic playlists for
each directory.

namestrip
---------
Written in Python. Given a directory it batch renames files based on a
given criteria. For instance, providing "alpha" as criteria will
rename files to only contain alpha characters.  Originally written
because I wanted to remove the Chinese characters from a few hundred
audio files.

mpcpl_time
----------
Written in Python. Given the path to a Media Player Classic playlist
file, it will calculate the total duration of the playlist. For some
reason MPC does not display this information (or at least, makes it
difficult to find how to display it!).

mpcpl_time uses the library hsaudiotag3k 1.1.3, which can be installed via pip.

recipe_adjuster
---------------
Written in Python. Given a recipe (either from a file or standard
input) and a ratio, it will adjust accordingly and print the new recipe.

Recipes entered via standard input must be in quotes and comma
separated: "2 cups flour, 1 cup sugar, 2 eggs". Recipes in a file must
have one ingredient per line.

subchecker
----------
Written in Python. Given a subtitle file and a specification file,
subchecker will check to see if the subtitles meet the requirements
defined in the specification file.

Each requirement in a specification file must be in the following format:
> KEY: value

Currently, subchecker can only ensure that subtitles do not exceed a
certain time or a certain amount of characters. Use the keys MAX_CHARS
and MAX_TIME to define either in your specification file.

For now only .srt files are supported.
