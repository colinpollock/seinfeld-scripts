"""Script for downloading Seinfeld scripts."""

from __future__ import division
import argparse
import os
import sys
import time

import requests



def _format_num(n):
    return '%02d' % n

EPISODE_NUMBERS = (
    list(map(_format_num, range(1, 82))) +

    # Double episode
    ['82and83'] +

    list(map(_format_num, range(84, 100))) +

    # Skip the clip show "100and101".

    list(map(_format_num, range(102, 177))) +

    # Skip the clip show "177and178".

    # Double episode (Finale)
    ['179and180']
)

URL = 'http://web.archive.org/web/20170707014801/http://www.seinology.com/scripts/script-%s.shtml'


def get_script_html(episode_number):
    url = URL % episode_number
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.text


def main(args):
    episode_numbers = (
        args.episode_number if args.episode_number is not None
        else EPISODE_NUMBERS
    )

    num_episodes = len(episode_numbers)
    for idx, episode_number in enumerate(episode_numbers, start=1):
        print('[Ep. %s]\t\t%d of %d (%.2f%%)' %  (
            episode_number, idx,
            len(episode_numbers),
            idx / num_episodes * 100
        ))

        out_path = os.path.join(
            args.output_directory,
            '%s.shtml' % episode_number
        )


        if args.no_overwrite is True and os.path.exists(out_path):
            continue

        script_html = get_script_html(episode_number)

        with open(out_path, 'w') as fh:
            fh.write(script_html)

        if idx != num_episodes:
            time.sleep(args.sleep_seconds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'output_directory',
        help='The directory to write script HTML files to.'
    )

    parser.add_argument(
        '--sleep-seconds',
        type=float,
        default=1.0,
        help=('The number of seconds to sleep between downloading each page. '
              'Defaults to 1 second.')
    )

    parser.add_argument(
        '--no-overwrite',
        action='store_false',
        default=True,
        help='If True then will not overwrite existing downloaded files.'
    )

    parser.add_argument(
        '--episode-number',
        action='append',
        required=False,
        choices=EPISODE_NUMBERS,
        help=('An episode name or number (e.g. "79" or "82and83"). If '
              'specified then only this episode will be downloaded '
              'rather than all of them (the default). This can be specified '
              'multiple times.')
    )

    main(parser.parse_args(sys.argv[1:]))
