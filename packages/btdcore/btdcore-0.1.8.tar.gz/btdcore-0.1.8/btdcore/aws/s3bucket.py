import logging
from typing import Iterable

import botocore.exceptions

from btdcore.aws.core import AwsServiceSession


s3 = AwsServiceSession("s3")


class S3Bucket:
    def __init__(self, *, bucket_name: str):
        self.bucket_name = bucket_name
        return

    def list_keys(
        self,
        *,
        prefix: str | None = None,
    ) -> Iterable[str]:
        kwargs = {
            "Bucket": self.bucket_name,
        }
        if prefix:
            kwargs["Prefix"] = prefix
            pass

        paginator = s3.service.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(**kwargs)
        for page in page_iterator:
            for item in page["Contents"]:
                yield item["Key"]
                pass
            pass
        return

    def write_to_key(
        self,
        *,
        key: str,
        contents: bytes,
    ):
        return s3.service.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=contents,
        )

    def read_at_key(self, key: str) -> bytes:
        r: dict
        try:
            r = s3.service.get_object(
                Bucket=self.bucket_name,
                Key=key,
            )
        except Exception as e:
            logging.error(
                "failed to fetch from S3 bucket %s key %s - %s",
                self.bucket_name,
                key,
                e,
            )
            raise e
        return b"".join(list(r["Body"]))

    def get_signed_download_url(self, key: str) -> str:
        return s3.service.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
            },
        )

    def key_exists(self, key: str) -> bool:
        try:
            s3.service.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            elif e.response["Error"]["Code"] == 403:
                return False
            else:
                raise e
            pass
        pass

    pass
