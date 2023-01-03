import argparse
import logging
from libreelec_torrent_linker.utils import Utils
from libreelec_torrent_linker.movie_linker import MovieScanner, MovieLinker
from libreelec_torrent_linker.tv_show_linker import TvShowEpisodeLinker, TvShowEpisodeScanner, TvShowSeasonLinker, TvShowSeasonScanner


def link(movies_path, tv_shows_path, downloads_path):
    Utils.init_directories(movies_path, tv_shows_path)

    _movie_linker = MovieLinker(movies_path, MovieScanner(downloads_path))
    _movie_linker.link()

    episode_linker = TvShowEpisodeLinker(tv_shows_path, TvShowEpisodeScanner(downloads_path))
    episode_linker.link()

    season_linker = TvShowSeasonLinker(tv_shows_path, TvShowSeasonScanner(downloads_path))
    season_linker.link()


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
        help="Absolute path to directory where you will store symbolic links. This directory is the source directory of video source in LibreELEC."
    )
    parser.add_argument(
        '--tv-shows-path',
        required=True,
        help="Absolute path to directory where you will store symbolic links. This directory is the source directory of video source in LibreELEC."
    )
    parser.add_argument(
        '--log-level',
        default="INFO",
        choices=["ERROR", "DEBUG", "INFO"]
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.getLevelName(args.log_level))
    link(
        movies_path=args.movies_path,
        downloads_path=args.downloads_path,
        tv_shows_path=args.tv_shows_path,
    )


if __name__ == "__main__":
    main()
