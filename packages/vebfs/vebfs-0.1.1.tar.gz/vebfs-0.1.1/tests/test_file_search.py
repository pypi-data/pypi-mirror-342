import unittest
import os
import tempfile
from vebfs import find_files, find_directories

class TestFileSearch(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        os.makedirs(os.path.join(self.test_dir.name, "subdir"))
        with open(os.path.join(self.test_dir.name, "file.txt"), "w") as f:
            f.write("content")
        with open(os.path.join(self.test_dir.name, "subdir", "note.md"), "w") as f:
            f.write("note")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_find_files(self):
        result = find_files(self.test_dir.name, "*.txt")
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].endswith("file.txt"))

    def test_find_directories(self):
        result = find_directories(self.test_dir.name, "subdir")
        self.assertEqual(len(result), 1)
        self.assertTrue("subdir" in result[0])

if __name__ == '__main__':
    unittest.main()
