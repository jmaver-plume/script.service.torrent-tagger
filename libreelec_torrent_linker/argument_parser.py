import argparse


def argument_parser():
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
    return parser