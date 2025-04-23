# Superfile

Simple Python file-like interface for cloud block storage. This is unlikely to be the most
performant way do I/O with data from block storage, but it provides a uniform, simple API that can
be used across multiple cloud block storage providers such as Google Cloud Storage, Amazon S3 and
Azure Blob Storage.

## Simple Usage

Importing the main module:

```python
import superfile
```

Reading a local file:

```python
with superfile.open('my/local/path', 'r') as f:
  contents = f.read()
```

Reading a text file:

```python
with superfile.open('gs://my_bucket_name/file.txt', 'r') as f:
  text = f.read()
```

Reading a binary file:

```python
with superfile.open('gs://my_bucket_name/file.ext', 'rb') as f:
  data = f.read()
```

Writing a text file:

```python
text = 'hello world'
with superfile.open('gs://my_bucket_name/file.txt', 'w') as f:
  f.write(text)
```

Writing a binary file:

```python
data = b'hello world'
with superfile.open('gs://my_bucket_name/file.txt', 'wb') as f:
  f.write(data)
```

Listing all files in a bucket:

```python
fnames = list(superfile.list('gs://my_bucket_name'))
```

Listing files with a prefix from a bucket:

```python
prefix = 'abc'
fnames = list(superfile.list(f'gs://my_bucket_name/{prefix}'))
```

## Advanced Usage

Reading a file from GCS and providing auth credentials:

```python
import superfile
from google.oauth2 import service_account

fpath = 'gs://my_bucket_name/file.txt'
creds = service_account.Credentials.from_service_account_file('/path/to/key.json')
with superfile.open(
  path=fpath,
  mode='r',
  # All init_kwargs are passed to google.cloud.storage.Client.__init__().
  init_kwargs=dict(credentials=creds),
  # All open_kwargs are passed to google.cloud.storage.Blob.open().
  open_kwargs=dict(errors='strict'),
) as f:
  ...
```

Reading a file from S3 and providing endpoint URL:

```python
import superfile

fpath = 's3://my_bucket_name/file.txt'
endpoint_url = 'https://example.com'
with superfile.open(
  path=fpath,
  mode='r',
  # All init_kwargs are passed to boto3.client().
  init_kwargs=dict(endpoint_url=endpoint_url),
  # All open_kwargs are passed to boto3.client.get_object() or boto3.client.put_object().
  open_kwargs=dict(VersionId='...'),
) as f:
  ...

```
