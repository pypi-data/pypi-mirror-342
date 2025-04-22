import json
import time
from uuid import uuid4
from urllib.parse import quote_plus

from btdcore.aws.core import AwsServiceSession
from btdcore.rest_client_base import PersistableRequestMetadata, RequestPersister
from btdcore.utils import map_multithreaded


class RequestPersisterS3(RequestPersister):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = AwsServiceSession("s3")
        return

    def _persist_single(self, req_metadata: PersistableRequestMetadata) -> None:
        key = "/".join(
            map(
                quote_plus,
                [
                    req_metadata.response_at_ts.strftime("%Y-%m-%d"),
                    f"{int(time.time())}-{uuid4()}",
                ],
            )
        )
        self.s3.service.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=req_metadata.to_json().encode("utf-8"),
        )
        return

    def persist(self, batch: list[PersistableRequestMetadata]):
        map_multithreaded(self._persist_single, batch, len(batch))
        return

    pass
