import os
import tempfile
from pathlib import Path

import boto3

from src.utils import check_env_vars, measure_network_speed

check_env_vars()

REPO_DIRPATH = Path(__file__).parents[1]
FILENAME = "large_file.bin"
DATA_FILEPATH = REPO_DIRPATH / "data" / FILENAME
S3_FILEPATH = f"s3://{os.environ['S3_BUCKET_NAME']}/{FILENAME}"


def _create_file_locally():
    file_size_in_gb = 3
    with open(DATA_FILEPATH, "wb") as f:
        f.seek(file_size_in_gb * int(1e9) - 1)
        f.write(b"\0")


def _get_bucket():
    session = boto3.Session()
    s3 = session.resource("s3")
    return s3.Bucket(os.environ["S3_BUCKET_NAME"])


def _upload_file():
    bucket = _get_bucket()
    bucket.upload_file(str(DATA_FILEPATH), str(S3_FILEPATH))


def create_large_file(upload: bool = True):
    _create_file_locally()
    if upload:
        _upload_file()


def benchmark_s3_download():
    bucket = _get_bucket()
    with tempfile.TemporaryDirectory() as tmp_dirpath:
        with measure_network_speed():
            bucket.download_file(str(S3_FILEPATH), f"{tmp_dirpath}/tmp.bin")
