import unittest
from FileReader import FileReader


class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.dir_path = r'./data'  # 数据目录路径
        self.file_reader = FileReader(self.dir_path, window_size=10, sample_freq=100)

    def test_read_files(self):
        # 读取2020-01-01的数据
        buffer_matrix = self.file_reader.read_files('2020-01-01')

        # 验证返回的矩阵大小
        self.assertEqual(buffer_matrix.shape, (15000, 5))

        # 验证Buffer1的大小是否正确
        self.assertEqual(self.file_reader.buffer1.shape, (1000, 1))

        # 读取2020-01-02的数据,Buffer1应更新,大小不变
        buffer_matrix = self.file_reader.read_files('2020-01-02')
        self.assertEqual(self.file_reader.buffer1.shape, (1000, 1))

        # 再读取2020-01-01的数据,Buffer1应重置,只包含这一天的数据
        buffer_matrix = self.file_reader.read_files('2020-01-01')
        self.assertEqual(self.file_reader.buffer1.shape, (1000, 1))

    def test_init_buffer(self):
        # 检验初始化的Buffer大小是否正确
        self.assertEqual(self.file_reader.buffer1.shape, (1000, 1))
        self.assertEqual(self.file_reader.buffer2.shape, (1000, 1))
        ...


if __name__ == '__main__':
    unittest.main()