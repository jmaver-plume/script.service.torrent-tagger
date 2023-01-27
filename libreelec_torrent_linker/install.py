import logging
import os

from libreelec_torrent_linker.argument_parser import argument_parser


def setup_cron(args):
    log = logging.getLogger('CronSetup')
    every_10_th_minute = '*/1 * * * *'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(script_dir, 'linker.py')
    arguments = f"--action='RunScript({script}, --downloads-path, {args.downloads_path}, --movies-path, {args.movies_path}, --tv-shows-path, {args.tv_shows_path}, --log-level, {args.log_level})'"
    function = '/usr/bin/kodi-send'
    expression = f'{every_10_th_minute} {function} {arguments}'
    cron_dir = '/storage/.cache/cron/crontabs/root'
    with open(cron_dir, 'w') as f:
        f.write(expression)
    log.debug(f'Wrote "{expression}" to "{cron_dir}"')


def main():
    parser = argument_parser()
    args = parser.parse_args()
    setup_cron(args)


if __name__ == "__main__":
    main()
