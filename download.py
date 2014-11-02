"""Script for downloading Seinfeld scripts."""

import argparse
import os
import sys

import requests


URL = 'http://www.seinology.com/scripts/script-%s.shtml'

def get_script_html(episode_number):
    url = URL % episode_number
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.text

def format_num(n):
    return '%02d' % n

episode_numbers = (
    map(format_num, range(1, 82)) + 

    # Double episode
    ['82and83'] +

    map(format_num, range(84, 100)) + 

    # Skip the clip show "100and101".

    map(format_num, range(102, 177)) + 

    # Skip the clip show "177and178".

    # Double episode (Finale)
    ['179and180']
)
num_episodes = len(episode_numbers)



def main(args):
    for idx, episode_number in enumerate(episode_numbers, start=1):
        print >> sys.stderr, '[Ep. %s]\t%d of %d (%.2f%%)' %  \
            (episode_number, idx, num_episodes, 10.0 * idx / num_episodes)

        script_html = get_script_html(episode_number)

        out_path = os.path.join(
            args.output_directory,
            '%s.shtml' % episode_number
        )

        with open(out_path, 'w') as fh:
            print >> fh, script_html


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'output_directory',
        help='The directory to write script HTML files to.'
    )

    main(parser.parse_args(sys.argv[1:]))
