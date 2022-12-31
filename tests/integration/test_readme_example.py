import pathlib
import unittest
import os

from src.libreelec_torrent_renamer import main


class TestIsMovieDir(unittest.TestCase):
    def test_should_create_new_directories(self):
        downloads_path = os.path.abspath('downloads')
        movies_symbolic_path = os.path.abspath('/tmp/directories/movies')
        tv_shows_symbolic_path = os.path.abspath('/tmp/directories/tv_shows')
        main(downloads_path, movies_symbolic_path, tv_shows_symbolic_path)

        # Validate movies
        self.assertTrue(os.path.exists(movies_symbolic_path))
        self.assertTrue(os.path.exists(f'{movies_symbolic_path}/Glass Onion A Knives Out Mystery (2022)'))
        self.assertTrue(os.path.islink(f'{movies_symbolic_path}/Glass Onion A Knives Out Mystery (2022)/Glass Onion A Knives Out Mystery (2022).mp4'))
        self.assertTrue(os.path.islink(f'{movies_symbolic_path}/Glass Onion A Knives Out Mystery (2022)/Subs'))

        # Validate TV Show Season
        self.assertTrue(os.path.exists(tv_shows_symbolic_path))
        self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/Counterpart'))
        self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/Counterpart/Season 1'))
        self.assertTrue(os.path.islink(f'{tv_shows_symbolic_path}/Counterpart/Season 1/Counterpart S01E01.mkv'))
        self.assertTrue(os.path.islink(f'{tv_shows_symbolic_path}/Counterpart/Season 1/Counterpart S01E02.mkv'))
        self.assertTrue(os.path.islink(f'{tv_shows_symbolic_path}/Counterpart/Season 1/Counterpart S01E03.mkv'))

        # # Validate TV Show Episode
        self.assertTrue(os.path.exists(tv_shows_symbolic_path))
        self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/The Patient'))
        self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/The Patient/Season 1'))
        self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/The Patient/Season 1/The Patient S01E02.mkv'))
        self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/The Patient/Season 1/The Patient S01E03.mp4'))
        # TODO: Not working, fix.
        # self.assertTrue(os.path.exists(f'{tv_shows_symbolic_path}/The Patient/Season 1/The Patient S01E03_2_English.srt'))


if __name__ == '__main__':
    unittest.main()
