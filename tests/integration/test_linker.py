import pathlib
import unittest
import os
from distutils.dir_util import copy_tree

import resources.lib.linker


class TestLinker(unittest.TestCase):

    def setUp(self):
        downloads_path = os.path.abspath(f'{pathlib.Path(__file__).parent.resolve()}/torrent_downloads')
        self.downloads_path = os.path.abspath('/tmp/directories/downloads')
        copy_tree(downloads_path, self.downloads_path)
        self.downloads_state_path = os.path.abspath(f'/tmp/libreelec-torrent-linker')
        self.movies_path = os.path.abspath('/tmp/directories/movies')
        self.tv_shows_path = os.path.abspath('/tmp/directories/tv_shows')

        resources.lib.linker.Utils.safe_delete_directory(self.tv_shows_path)
        resources.lib.linker.Utils.safe_delete_directory(self.movies_path)

        if os.path.exists(self.downloads_state_path):
            os.remove(self.downloads_state_path)

    def test_should_create_new_directories_and_link_files_and_set_state_when_empty(self):
        class MockPlayer:
            def isPlaying(self):
                return False

        class MockXbmc:
            @staticmethod
            def executebuiltin(arg):
                pass

            @staticmethod
            def Player():
                return MockPlayer()


        linker = resources.lib.linker.Linker(
            downloads_path=self.downloads_path,
            downloads_state_path=self.downloads_state_path,
            movies_path=self.movies_path,
            tv_shows_path=self.tv_shows_path,
            xbmc=MockXbmc
        )
        linker.link()

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

        # Validate Alice in Borderland
        self.assertTrue(os.path.exists(self.tv_shows_path))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/Alice in Borderland'))
        self.assertTrue(os.path.exists(f'{self.tv_shows_path}/Alice in Borderland/Season 1'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/Alice in Borderland/Season 1/Alice in Borderland S01E01.mp4'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/Alice in Borderland/Season 1/Alice in Borderland S01E02.mp4'))
        self.assertTrue(os.path.islink(f'{self.tv_shows_path}/Alice in Borderland/Season 1/Subs'))

        os.remove(self.downloads_state_path)

    def test_should_quit_early_when_player_is_playing(self):
        class MockPlayer:
            def isPlaying(self):
                return True

        class MockXbmc:
            @staticmethod
            def executebuiltin():
                pass

            @staticmethod
            def Player():
                return MockPlayer()

        linker = resources.lib.linker.Linker(
            downloads_path=self.downloads_path,
            downloads_state_path=self.downloads_state_path,
            movies_path=self.movies_path,
            tv_shows_path=self.tv_shows_path,
            xbmc=MockXbmc
        )
        linker.link()

        self.assertFalse(os.path.exists(self.movies_path))
        self.assertFalse(os.path.exists(self.tv_shows_path))

    def test_should_quit_early_downloads_state_is_the_same(self):
        class MockPlayer:
            def isPlaying(self):
                return False

        class MockXbmc:
            @staticmethod
            def executebuiltin(arg):
                pass

            @staticmethod
            def Player():
                return MockPlayer()

        linker = resources.lib.linker.Linker(
            downloads_path=self.downloads_path,
            downloads_state_path=self.downloads_state_path,
            movies_path=self.movies_path,
            tv_shows_path=self.tv_shows_path,
            xbmc=MockXbmc
        )
        linker.link()
        linker.link() # TODO: How to test?

    @unittest.skip('Not implemented')
    def test_should_call_kodi_library_cleanup_if_old_deleted(self):
        pass

    @unittest.skip('Not implemented')
    def test_should_call_kodi_library_update_if_new_added(self):
        pass


if __name__ == '__main__':
    unittest.main()
