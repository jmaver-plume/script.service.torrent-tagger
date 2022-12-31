import unittest

from src.libreelec_torrent_renamer import get_movie_name


class TestGetMovieName(unittest.TestCase):
    def test_should_return_movie_name(self):
        self.assertEqual(get_movie_name('Knives.Out.2019.2160p.BluRay.HEVC.TrueHD.7.1.Atmos-EATDIK'), "Knives Out (2019)")


if __name__ == '__main__':
    unittest.main()
