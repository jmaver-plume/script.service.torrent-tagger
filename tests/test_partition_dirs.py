import unittest

from main import partition_dirs


class TestPartitionDirs(unittest.TestCase):
    def test_partition_dirs(self):
        dirs = ['Strange.World.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX', 'The.Patient.S01.WEBRip.x265-ION265', 'Nothing']
        tv_show_dirs, movie_dirs = partition_dirs(dirs)
        self.assertEqual(tv_show_dirs, ['The.Patient.S01.WEBRip.x265-ION265'])


if __name__ == '__main__':
    unittest.main()
