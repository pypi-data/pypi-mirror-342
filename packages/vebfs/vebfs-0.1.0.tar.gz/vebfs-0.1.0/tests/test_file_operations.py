import unittest
import os
import tempfile
from fsutils import (
    copy_file, move_file, delete_file, delete_directory,
    create_backup, get_file_size, list_all_files, ensure_directory_exists
)

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.test_dir.name, "file.txt")
        with open(self.file_path, 'w') as f:
            f.write("test")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_copy_file(self):
        dest_path = os.path.join(self.test_dir.name, "copy.txt")
        copy_file(self.file_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))

    def test_move_file(self):
        dest_path = os.path.join(self.test_dir.name, "moved.txt")
        move_file(self.file_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))
        self.assertFalse(os.path.exists(self.file_path))

    def test_delete_file(self):
        delete_file(self.file_path)
        self.assertFalse(os.path.exists(self.file_path))

    def test_delete_directory_recursive(self):
        sub_dir = os.path.join(self.test_dir.name, "subdir")
        os.makedirs(sub_dir)
        delete_directory(sub_dir, recursive=True)
        self.assertFalse(os.path.exists(sub_dir))

    def test_create_backup(self):
        backup_path = os.path.join(self.test_dir.name, "backup.txt")
        create_backup(self.file_path, backup_path)
        self.assertTrue(os.path.exists(backup_path))

    def test_get_file_size(self):
        size = get_file_size(self.file_path)
        self.assertEqual(size, 4)

    def test_list_all_files(self):
        files = list_all_files(self.test_dir.name)
        self.assertIn(self.file_path, files)

    def test_ensure_directory_exists(self):
        new_dir = os.path.join(self.test_dir.name, "newdir")
        ensure_directory_exists(new_dir)
        self.assertTrue(os.path.exists(new_dir))

if __name__ == '__main__':
    unittest.main()
