#!/usr/bin/python

import argparse
import logging
import os


def setup_cron(args):
    log = logging.getLogger('CronSetup')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(script_dir, 'libreelec_torrent_linker/linker.py')
    arguments = (
        f"--action='RunScript({script}, --downloads-path, {args.downloads_path}, "
        f"--movies-path, {args.movies_path}, --tv-shows-path, {args.tv_shows_path}, "
        f"--log-level, {args.log_level})'"
    )
    function = '/usr/bin/kodi-send'
    expression = f'{args.cron_expression} {function} {arguments}'
    cron_dir = '/storage/.cache/cron/crontabs/root'
    with open(cron_dir, 'w') as f:
        f.write(expression)
    log.debug(f'Wrote "{expression}" to "{cron_dir}"')


def main():
    parser = argparse.ArgumentParser(description='Creates symbolic links with proper naming for LibreELEC scraper.')
    parser.add_argument(
        '--downloads-path',
        required=True,
        help="Absolute path to directory where you have downloaded torrents."
    )
    parser.add_argument(
        '--movies-path',
        required=True,
        help=("Absolute path to directory where you will store symbolic links. "
              "This directory is the source directory of video source in LibreELEC.")
    )
    parser.add_argument(
        '--tv-shows-path',
        required=True,
        help=("Absolute path to directory where you will store symbolic links. "
              "This directory is the source directory of video source in LibreELEC.")
    )
    parser.add_argument(
        '--log-level',
        default="INFO",
        choices=["ERROR", "DEBUG", "INFO"]
    )
    parser.add_argument(
        '--cron-expression',
        default="*/30 * * * *",
    )
    args = parser.parse_args()
    setup_cron(args)


if __name__ == "__main__":
    main()
