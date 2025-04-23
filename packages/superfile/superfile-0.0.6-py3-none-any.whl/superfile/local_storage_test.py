import pathlib
import tempfile
import unittest
from . import superfile


def _create_files(paths: list[str]) -> tempfile.TemporaryDirectory:
  tmpdir = tempfile.TemporaryDirectory()
  root = pathlib.Path(tmpdir.name)
  for fpath in paths:
    fpath = root / fpath
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.touch()
  return tmpdir


class TestLocalStorage(unittest.TestCase):

  def test_write_text_file(self):
    text = "hello world"
    with tempfile.TemporaryDirectory() as tmpdir:
      fpath = tmpdir + "/" + "test.txt"
      with superfile.open(fpath, "w") as f:
        f.write(text)
      with open(fpath, "r") as f:
        self.assertEqual(f.read(), text)

  def test_read_text_file(self):
    text = "hello world"
    with tempfile.TemporaryDirectory() as tmpdir:
      fpath = tmpdir + "/" + "test.txt"
      with open(fpath, "w") as f:
        f.write(text)
      with superfile.open(fpath, "r") as f:
        self.assertEqual(f.read(), text)

  def test_read_text_file_from_path(self):
    text = "hello world"
    with tempfile.TemporaryDirectory() as tmpdir:
      fpath = pathlib.Path(tmpdir) / "test.txt"
      with open(fpath, "w") as f:
        f.write(text)
      with superfile.open(fpath, "r") as f:
        self.assertEqual(f.read(), text)

  def test_list_all_files_with_prefix(self):
    fpaths = [
        "file_0.txt",
        "subdir/file_1.txt",
        "subdir/subsubdir/file_2.txt",
        "subdir/subsubdir/file_3.txt",
    ]
    with _create_files(fpaths) as tmpdir:
      inputs = [tmpdir + "/" + x for x in fpaths]

      result = list(superfile.list(tmpdir))
      self.assertListEqual(result, inputs)

      mismatch = list(superfile.list(tmpdir + "_"))
      self.assertListEqual(mismatch, [])

  def test_list_all_files_with_glob(self):
    fpaths = [
        "file_0.txt",
        "subdir/file_1.txt",
        "subdir/subsubdir/file_2.txt",
        "subdir/subsubdir/file_3.txt",
    ]
    with _create_files(fpaths) as tmpdir:
      inputs = [tmpdir + "/" + x for x in fpaths]

      result = list(superfile.list(tmpdir + "/*"))
      self.assertListEqual(result, inputs)

      mismatch = list(superfile.list(tmpdir + "_" + "/*"))
      self.assertListEqual(mismatch, [])

  def test_files_exist(self):
    fpaths = [
        "file_0.txt",
        "subdir/file_1.txt",
        "subdir/subsubdir/file_2.txt",
        "subdir/subsubdir/file_3.txt",
    ]
    with _create_files(fpaths) as tmpdir:
      inputs = [tmpdir + "/" + x for x in fpaths]

      for fpath in inputs:
        self.assertTrue(superfile.exists(fpath))

  def test_write_to_non_existing_subdirectory(self):
    text = "hello world"
    with tempfile.TemporaryDirectory() as tmpdir:
      fpath = tmpdir + "/" + "subdir" + "/" + "test.txt"
      with superfile.open(fpath, "w") as f:
        f.write(text)
      with open(fpath, "r") as f:
        self.assertEqual(f.read(), text)


if __name__ == "__main__":
  unittest.main()
