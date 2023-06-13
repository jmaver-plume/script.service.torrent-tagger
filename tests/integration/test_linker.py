import os
import pathlib
import unittest
from distutils.dir_util import copy_tree

from resources.lib.linker import Linker, MovieLinker, MovieScanner, TvShowLinker, TvShowEpisodeScanner, \
    DownloadsDirectory, Utils, TvShowSeasonScanner, Logger


class MockXbmc:
    LOGDEBUG = 1
    LOGINFO = 1
    LOGERROR = 1

    @staticmethod
    def executebuiltin(arg):
        pass

    @staticmethod
    def executeJSONRPC(arg):
        return '{"result": {"tvshows": []}}'

    @staticmethod
    def log(msg, level):
        pass


class TestLinker(unittest.TestCase):

    def setUp(self):
        downloads_path = os.path.abspath(f'{pathlib.Path(__file__).parent.resolve()}/torrent_downloads')
        self.downloads_path = os.path.abspath('/tmp/directories/downloads')
        self.downloads_state_path = os.path.abspath('/tmp/libreelec-torrent-linker')
        self.movies_path = os.path.abspath('/tmp/directories/movies')
        self.tv_shows_path = os.path.abspath('/tmp/directories/tv_shows')

        self.logger = Logger(MockXbmc)
        self.utils = Utils(self.logger)
        self.utils.safe_delete_directory(self.tv_shows_path)
        self.utils.safe_delete_directory(self.movies_path)

        movie_scanner = MovieScanner(downloads_path, self.logger)
        tv_show_episode_scanner = TvShowEpisodeScanner(downloads_path, self.logger)
        tv_show_season_scanner = TvShowSeasonScanner(downloads_path, self.logger)
        downloads_directory = DownloadsDirectory(downloads_path, self.downloads_state_path, self.logger)
        movie_linker = MovieLinker(self.movies_path, movie_scanner, self.logger, self.utils)
        episode_linker = TvShowLinker(self.tv_shows_path, tv_show_episode_scanner, self.logger, self.utils)
        season_linker = TvShowLinker(self.tv_shows_path, tv_show_season_scanner, self.logger, self.utils)

        self.linker = Linker(
            tv_shows_path=self.tv_shows_path,
            downloads_path=downloads_path,
            movies_path=self.movies_path,
            downloads_state_path=self.downloads_state_path,
            xbmc=MockXbmc,
            logger=self.logger,
            movie_linker=movie_linker,
            episode_linker=episode_linker,
            season_linker=season_linker,
            downloads_directory=downloads_directory,
            utils=self.utils
        )

        copy_tree(downloads_path, self.downloads_path)
        if os.path.exists(self.downloads_state_path):
            os.remove(self.downloads_state_path)

    def test_should_create_new_directories_and_link_files_and_set_state_when_empty(self):
        self.linker.link()

        # Validate movies
        self.assertTrue(os.path.exists(self.movies_path))
        self.assertTrue(os.path.exists(f'{self.movies_path}/Glass Onion A Knives Out Mystery (2022)'))
        self.assertTrue(os.path.islink(
            f'{self.movies_path}/Glass Onion A Knives Out Mystery (2022)/Glass Onion A Knives Out Mystery (2022).mp4'))
        self.assertTrue(os.path.islink(f'{self.movies_path}/Glass Onion A Knives Out Mystery (2022)/Subs'))

        # Validate TV Show Season
        self.assertTrue(os.path.exists(self.tv_shows_path))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/Counterpart'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/Counterpart/Season 1'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/Counterpart/Season 1/Counterpart S01E01.mkv'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/Counterpart/Season 1/Counterpart S01E02.mkv'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/Counterpart/Season 1/Counterpart S01E03.mkv'))

        # Validate TV Show Season - The Glory
        self.assertTrue(os.path.exists(self.tv_shows_path))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Glory (2022)'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Glory (2022)/Season 1'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/The Glory (2022)/Season 1/The Glory (2022) S01E01.mkv'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/The Glory (2022)/Season 1/The Glory (2022) S01E02.mkv'))

        # Validate TV Show Episode
        self.assertTrue(os.path.exists(self.tv_shows_path))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Patient'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Patient/Season 1'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/The Patient/Season 1/The Patient S01E02.mkv'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/The Patient/Season 1/The Patient S01E03.mp4'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Patient/Season 1/The Patient S01E03 Subs'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/The Patient/Season 1/The Patient S01E04.mp4'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Patient/Season 1/The Patient S01E04 2_English.srt'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/The Patient/Season 1/The Patient S01E04 3_English.srt'))

        os.remove(self.downloads_state_path)


if __name__ == '__main__':
    unittest.main()
