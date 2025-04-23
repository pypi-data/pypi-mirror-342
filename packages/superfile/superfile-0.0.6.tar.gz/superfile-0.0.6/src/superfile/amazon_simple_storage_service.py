from typing import IO, Iterable
import boto3
from mypy_boto3_s3.client import S3Client
from . import interfaces


class _S3FileObject(interfaces.FileLike):

  def __init__(
      self,
      client: S3Client,
      uri: interfaces.FileURI,
      mode: interfaces.FileMode,
      encoding: str | None = None,
      **kwargs,
  ):
    self.client = client
    self.kwargs = kwargs
    super().__init__(uri, mode, encoding)

  def read(self, **kwargs) -> str | bytes:
    obj = self.client.get_object(
        Bucket=self.uri.bucket,
        Key=self.uri.subpath,
        **kwargs,
    )
    data = obj["Body"].read()
    return data if self.mode[-1] == "b" else data.decode(self.encoding)

  def write(self, data: str | bytes, **kwargs) -> None:
    _ = self.client.put_object(
        Bucket=self.uri.bucket,
        Key=self.uri.subpath,
        Body=data,
        **kwargs,
    )
    return

  def close(self) -> None:
    ...

  def exists(self, **kwargs) -> bool:
    return self.client.head_object(
        Bucket=self.uri.bucket,
        Key=self.uri.subpath,
        **kwargs,
    )


class S3File(interfaces.SuperFile):
  scheme = "s3"

  def __init__(self, **kwargs):
    self.client = boto3.client("s3", **kwargs)

  def open(
      self,
      path: str,
      mode: interfaces.FileMode = "r",
      **kwargs,
  ) -> interfaces.FileLike:
    uri = interfaces.FileURI.from_url(path, validate_scheme=S3File.scheme)
    return _S3FileObject(self.client, uri=uri, mode=mode)

  def list(self, path: str, **kwargs) -> Iterable[str]:
    uri = interfaces.FileURI.from_url(path, validate_scheme=S3File.scheme)
    res = self.client.list_objects_v2(
        Bucket=uri.bucket,
        Prefix=uri.subpath or "",
        **kwargs,
    )
    yield from (x["Key"] for x in res.get("Contents", []))

  def exists(self, path: str, **kwargs) -> bool:
    uri = interfaces.FileURI.from_url(path, validate_scheme=S3File.scheme)
    return _S3FileObject(self.client, uri=uri).exists(**kwargs)
