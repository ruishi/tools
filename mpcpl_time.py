"""Calculates and returns the total duration of a Media Player Classic
playlist."""

import sys
import os
from collections import OrderedDict

from hsaudiotag import auto

def main(playlist_path):
    audio_files = extract_filenames(playlist_path)
    total_seconds = calculate_seconds(playlist_path, audio_files)
    duration = calculate_duration_units(total_seconds)
    print_duration(duration)

def extract_filenames(playlist_path):
    with open(playlist_path) as f:
        filename_data = [line.strip() for line in f.readlines()
                         if 'filename' in line]
    # Each line with filename data has the following format:
    # <PlaylistTrackNumber>,filename,<filename or path>
    # So we just grab the relevant bit at the end:
    return [line.split(',')[-1] for line in filename_data]

def calculate_seconds(playlist_path, audio_files):
    playlist_dir_path = os.path.dirname(os.path.abspath(playlist_path))
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
    return total_seconds

def get_seconds(audio_file):
    audio_file = auto.File(audio_file)
    return audio_file.duration

def calculate_duration_units(total_seconds):
    duration = OrderedDict()
    total_minutes = total_seconds // 60
    duration['hours'] =  total_minutes // 60
    duration['minutes'] = total_minutes % 60
    duration['seconds'] = total_seconds % 60
    return duration


def print_duration(duration):
    print("Playlist duration:", end=' ')
    duration_str  = ''.join("{}{}".format(length, unit[0])
                             for unit, length in duration.items()
                             if length > 0)
    print(duration_str)

if __name__ == '__main__':
    main(sys.argv[1])
