import pathlib
import unittest
import os

import libreelec_torrent_linker


class TestLinker(unittest.TestCase):
    def test_should_create_new_directories_and_link_files(self):
        downloads_path = os.path.abspath(f'{pathlib.Path(__file__).parent.resolve()}/torrent_downloads')
        movies_path = os.path.abspath('/tmp/directories/movies')
        tv_shows_path = os.path.abspath('/tmp/directories/tv_shows')

        linker = libreelec_torrent_linker.Linker(
            downloads_path=downloads_path,
            movies_path=movies_path,
            tv_shows_path=tv_shows_path
        )
        linker.link()

        # Validate movies
        self.assertTrue(os.path.exists(movies_path))
        self.assertTrue(os.path.exists(f'{movies_path}/Glass Onion A Knives Out Mystery (2022)'))
        self.assertTrue(os.path.islink(
            f'{movies_path}/Glass Onion A Knives Out Mystery (2022)/Glass Onion A Knives Out Mystery (2022).mp4'))
        self.assertTrue(os.path.islink(f'{movies_path}/Glass Onion A Knives Out Mystery (2022)/Subs'))

        # Validate TV Show Season
        self.assertTrue(os.path.exists(tv_shows_path))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/Counterpart'))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/Counterpart/Season 1'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/Counterpart/Season 1/Counterpart S01E01.mkv'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/Counterpart/Season 1/Counterpart S01E02.mkv'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/Counterpart/Season 1/Counterpart S01E03.mkv'))

        # Validate TV Show Season - The Glory
        self.assertTrue(os.path.exists(tv_shows_path))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Glory (2022)'))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Glory (2022)/Season 1'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/The Glory (2022)/Season 1/The Glory (2022) S01E01.mkv'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/The Glory (2022)/Season 1/The Glory (2022) S01E02.mkv'))

        # # Validate TV Show Episode
        self.assertTrue(os.path.exists(tv_shows_path))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Patient'))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Patient/Season 1'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/The Patient/Season 1/The Patient S01E02.mkv'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/The Patient/Season 1/The Patient S01E03.mp4'))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Patient/Season 1/The Patient S01E03 Subs'))
        self.assertTrue(os.path.islink(f'{tv_shows_path}/The Patient/Season 1/The Patient S01E04.mp4'))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Patient/Season 1/The Patient S01E04 2_English.srt'))
        self.assertTrue(os.path.exists(f'{tv_shows_path}/The Patient/Season 1/The Patient S01E04 3_English.srt'))


if __name__ == '__main__':
    unittest.main()
