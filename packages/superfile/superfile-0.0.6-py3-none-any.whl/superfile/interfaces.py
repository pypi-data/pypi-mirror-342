import dataclasses
from types import TracebackType
from typing import IO, Iterable, Literal

FileMode = Literal["r", "rt", "rb", "w", "wt", "wb"]


@dataclasses.dataclass
class FileURI:
  scheme: str
  bucket: str
  subpath: str | None

  @staticmethod
  def from_url(url: str, validate_scheme: str | None = None) -> "FileURI":
    # Ensure url is a string.
    url = str(url) if url else url

    if "://" in url:
      scheme, fullpath = url.split("://", 1)
    else:
      scheme = "file"
      fullpath = url

    if validate_scheme and scheme != validate_scheme:
      raise ValueError(f"Invalid scheme: {scheme}.")

    if scheme == "file":
      return FileURI(scheme=scheme, bucket="", subpath=fullpath)

    else:
      parts = fullpath.split("/", 1)
      bucket = parts.pop(0)
      subpath = parts.pop(0) if parts else None
      return FileURI(scheme, bucket, subpath)


class FileLike:

  def __init__(
      self,
      uri: FileURI,
      mode: FileMode = "r",
      encoding: str | None = None,
  ):
    self.uri = uri
    self._mode = mode
    self.encoding = None
    if mode[-1] != "b":
      self.encoding = encoding or "utf-8"

  @property
  def mode(self):
    return self._mode

  def __enter__(self) -> "FileLike":
    return self

  def __exit__(
      self,
      exc_type: type[BaseException] | None,
      exc_value: BaseException | None,
      exc_traceback: TracebackType | None,
  ) -> None:
    ...

  def read(self, **kwargs) -> str | bytes:
    raise NotImplementedError()

  def write(self, data: str | bytes, **kwargs) -> None:
    raise NotImplementedError()

  def exists(self) -> bool:
    raise NotImplementedError()

  def close() -> None:
    ...


class SuperFile(object):

  def __init__(self):
    raise NotImplementedError()

  def open(self, path: str, mode: FileMode = "r", **kwargs) -> FileLike:
    raise NotImplementedError()

  def list(self, path: str, **kwargs) -> Iterable[str]:
    raise NotImplementedError()

  def delete(self, path: str, **kwargs) -> None:
    raise NotImplementedError()

  def exists(self, path: str, **kwargs) -> bool:
    raise NotImplementedError()
