import unittest

from src.libreelec_torrent_renamer import is_movie_dir


class TestIsMovieDir(unittest.TestCase):
    def test_1080p_is_movie_dir(self):
        self.assertEqual(is_movie_dir('Strange.World.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX'), True)
        self.assertEqual(is_movie_dir('High.Heat.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX'), True)
        self.assertEqual(is_movie_dir('Glass.Onion.A.Knives.Out.Mystery.2022.1080p.WEBRip.x265-RARBG'), True)

    def test_2160p_is_movie_dir(self):
        self.assertEqual(is_movie_dir('Knives.Out.2019.2160p.BluRay.HEVC.TrueHD.7.1.Atmos-EATDIK'), True)

    def test_720p_is_movie_dir(self):
        self.assertEqual(is_movie_dir('Knives.Out.2019.720p.BluRay.HEVC.TrueHD.7.1.Atmos-EATDIK'), True)


if __name__ == '__main__':
    unittest.main()
