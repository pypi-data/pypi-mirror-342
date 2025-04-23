from typing import Iterable

from google.cloud import storage

from . import interfaces


class GCSFile(interfaces.SuperFile):
  scheme = "gs"

  def __init__(self, **kwargs):
    self.client = storage.Client(**kwargs)

  def open(
      self,
      path: str,
      mode: interfaces.FileMode = "r",
      encoding: str | None = None,
      **kwargs,
  ) -> interfaces.FileLike:
    uri = interfaces.FileURI.from_url(path, validate_scheme=GCSFile.scheme)
    bucket = storage.Bucket(self.client, uri.bucket)
    blob = bucket.blob(uri.subpath)
    return blob.open(mode, encoding=encoding, **kwargs)

  def list(self, path: str, **kwargs) -> Iterable[str]:
    uri = interfaces.FileURI.from_url(path, validate_scheme=GCSFile.scheme)
    bucket = storage.Bucket(self.client, uri.bucket)
    blobs = bucket.list_blobs(prefix=uri.subpath or "", **kwargs)
    yield from (x.name for x in blobs)

  def exists(self, path: str, **kwargs) -> bool:
    uri = interfaces.FileURI.from_url(path, validate_scheme=GCSFile.scheme)
    bucket = storage.Bucket(self.client, uri.bucket)
    blob = bucket.blob(uri.subpath)
    return blob.exists(**kwargs)
