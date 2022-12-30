import unittest

from main import is_tv_show_dir


class TestIsTvShowDir(unittest.TestCase):
    def test_movie_is_not_tv_show_dir(self):
        self.assertEqual(is_tv_show_dir('Knives.Out.2019.2160p.BluRay.HEVC.TrueHD.7.1.Atmos-EATDIK'), False)
        self.assertEqual(is_tv_show_dir('Glass.Onion.A.Knives.Out.Mystery.2022.1080p.WEBRip.x265-RARBG'), False)
        self.assertEqual(is_tv_show_dir('Strange.World.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX'), False)
        self.assertEqual(is_tv_show_dir('High.Heat.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX'), False)

    def test_single_episode_is_tv_show_dir(self):
        self.assertEqual(is_tv_show_dir('The.Patient.S01E10.The.Cantors.Husband.1080p.DSNP.WEBRip.DDP5.1.x264-NTb[rartv]'), True)

    def test_season_is_tv_show_dir(self):
        self.assertEqual(is_tv_show_dir('The.Patient.S01.WEBRip.x265-ION265'), True)


if __name__ == '__main__':
    unittest.main()