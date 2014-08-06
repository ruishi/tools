"""Calculates and returns the total duration of a Media Player Classic
playlist."""

import sys
import os
from collections import namedtuple

from hsaudiotag import auto

Duration = namedtuple('Duration', ['minutes', 'seconds'])

def main(playlist_path):
    playlist_dir_path = os.path.dirname(os.path.abspath(playlist_path))
    with open(playlist_path) as f:
        filename_data = [line.strip() for line in f.readlines()
                         if 'filename' in line]
    # Each line with filename data has the following format:
    # <PlaylistTrackNumber>,filename,<filename or path>
    # So we just grab the relevant bit at the end:
    audio_files = [line.split(',')[-1] for line in filename_data]
    total_seconds = 0
    for audio_file in audio_files:
        # Sometimes the filename line just has the name
        # (e.g. '01.mp3') and sometimes it has the full path to the
        # audio file.
        # If it's the former, try appending the path to the directory of the
        # playlist to the name of the audio file.
        if os.path.isfile(audio_file):
            total_seconds += get_seconds(audio_file)
        else:
            new_file_path = os.path.join(playlist_dir_path, audio_file)
            if os.path.isfile(new_file_path):
                total_seconds += get_seconds(new_file_path)
            else:
                print("Could not locate file: {}".format(audio_file))
                continue

    duration = calculate_duration(total_seconds)
    print("Playlist duration: {} minutes, {} seconds".format(duration.minutes,
                                                             duration.seconds))

def get_seconds(audio_file):
    audio_file = auto.File(audio_file)
    return audio_file.duration

def calculate_duration(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return Duration(minutes, seconds)

if __name__ == '__main__':
    main(sys.argv[1])
