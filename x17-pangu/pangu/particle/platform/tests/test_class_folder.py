import unittest
from pangu.particle.platform.folder import Folder
from pangu.particle.platform.path import Path


class DummyPath(Path):
    def is_absolute(self):
        return True

    def is_remote(self):
        return False

    def to_uri(self):
        return self.raw


class DummyFolder(Folder):
    def list_files(self):
        return ["file1.txt", "file2.txt"]

    def list_folders(self):
        return ["subdir1", "subdir2"]

    def mkdir(self, exist_ok=True):
        return True


class TestFolder(unittest.TestCase):

    def test_repr(self):
        f = DummyFolder(DummyPath("/dir"))
        self.assertIn("DummyFolder", repr(f))

    def test_list_files(self):
        f = DummyFolder(DummyPath("/dir"))
        self.assertIn("file1.txt", f.list_files())

    def test_list_folders(self):
        f = DummyFolder(DummyPath("/dir"))
        self.assertIn("subdir2", f.list_folders())

    def test_mkdir(self):
        f = DummyFolder(DummyPath("/dir"))
        self.assertTrue(f.mkdir())

    def test_export(self):
        f = DummyFolder(DummyPath("/dir"))
        exported = f.export()
        self.assertEqual(exported["path"], "/dir")
        self.assertEqual(exported["path"], str(f.path))


if __name__ == "__main__":
    unittest.main()
