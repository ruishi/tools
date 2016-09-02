
"""Validates an .srt file based on specification file provided by user."""

import argparse
from collections import namedtuple
from datetime import timedelta

Subtitle = namedtuple('Subtitle', ['start', 'end', 'content'])

def chunk_srt(srt_filepath):
    """Extract relevant info from srt file

    Returns a list of Subtitle objects.

    """
    have_time = False
    blank_line = False
    subtitles = list()
    content = list()

    with open(srt_filepath, encoding="utf-8") as f:
        for line in f:
            if line.strip() == '':
                blank_line = True
            # timing data
            if "-->" in line:
                start, end = line.split(' --> ')
                have_time = True
            elif have_time and not blank_line:
                content.append(line)
            elif blank_line:
                subtitles.append(Subtitle(start, end.strip(),
                                          tuple(content)))
                have_time = False
                blank_line = False
                content.clear()

    return subtitles

def calc_screen_time(start, end):
    """Calculates amount of time subtitle is on screen

    Returns datetime.timedelta object"""
    start_parts = start.split(':')
    # use slicing to replace last entry with just seconds and append
    # milliseconds
    start_parts[-1::] = start_parts[-1].split(',')
    end_parts = end.split(':')
    end_parts[-1::] = end_parts[-1].split(',')

    start_parts = [int(t) for t in start_parts]
    end_parts = [int(t) for t in end_parts]

    start_delta = timedelta(hours=start_parts[0],
                            minutes=start_parts[1],
                            seconds=start_parts[2],
                            microseconds=start_parts[3] * 1000)

    end_delta = timedelta(hours=end_parts[0],
                          minutes=end_parts[1],
                          seconds=end_parts[2],
                          microseconds=end_parts[3] * 1000)

    return end_delta - start_delta

def calc_num_chars(subtitle):
    """Returns number of characters in a subtitle"""
    count = 0
    for line in subtitle:
        count += len(line.strip())
    return count


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('subs', type=str,
                        help="path to subtitle file")
    parser.add_argument('spec', type=str,
                        help="path to specification file")

    return vars(parser.parse_args())

def check_char_count(subtitles, max_chars):
    """Checks number of characters in each subtitle and prints line number
    of any violations.

    Returns number of violations.

    """
    if not max_chars:
        return
    violations = 0
    for idx, subtitle in enumerate(subtitles):
        char_count = calc_num_chars(subtitle.content)
        if char_count > max_chars:
            print("Line {}: Character count violation, {} characters".format(idx+1, char_count))
            violations += 1
    return violations

def check_duration(subtitles, min_time, max_time):
    """Checks the duration of each subtitle and prints line number of any
    violations.

    Returns number of time violations.

    """

    if not max_time and not min_time:
        return
    violations = 0
    for idx, subtitle in enumerate(subtitles):
        duration = calc_screen_time(subtitle.start, subtitle.end)
        if duration < min_time:
            print("Line {}: Min time violation, {} seconds".format(idx+1, duration))
            violations += 1
        elif duration > max_time:
            print("Line {}: Max time violation, {} seconds".format(idx+1, duration))
            violations += 1
    return violations

def validate(subtitles, spec):
    """Runs each specification check and reports failure count."""
    print(spec.get('MAX_TIME'), spec.get('MIN_TIME'))
    char_fails = check_char_count(subtitles, spec.get('MAX_CHARS'))
    time_fails = check_duration(subtitles, spec.get('MIN_TIME'), spec.get('MAX_TIME'))

    if time_fails == 0 and char_fails == 0:
        print("Subtitle requirements satisfied.")
    else:
        print("\n{} character count violations, {} time violations".format(char_fails, time_fails))

def to_timedelta(secs, millis):
    return timedelta(seconds=secs, microseconds=millis*100)

def main(subs, spec):
    subtitles = chunk_srt(subs)
    spec_dict = dict()
    with open(spec) as f:
        for line in f:
            key, val = line.split(':')
            if key == 'MIN_TIME' or key == 'MAX_TIME':
                secs, millis = [int(i) for i in val.split(',')]
                millis = millis * 100
                val = to_timedelta(secs, millis)
            else:
                val = int(val)
            spec_dict[key] = val
    validate(subtitles, spec_dict)


if __name__ == '__main__':
    main(**parse_args())
