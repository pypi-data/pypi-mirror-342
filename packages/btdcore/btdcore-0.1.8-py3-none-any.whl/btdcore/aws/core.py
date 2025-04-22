import base64
import json
import os
import subprocess
from typing import (
    Optional,
)

import boto3  # type: ignore
from botocore.config import Config  # type: ignore


DEFAULT_REGION = "us-east-2"


class AwsServiceSession:
    def __init__(
        self,
        service_name: str,
        *,
        profile: str | None = None,
        region_name: str | None = None,
        creds_bundle: Optional[str] = None,
    ):
        if not profile:
            profile = os.environ.get("AWS_PROFILE")
        if not region_name:
            region_name = os.environ.get("AWS_REGION", DEFAULT_REGION)
        self.service_name = service_name
        if creds_bundle:
            creds = json.loads(base64.b64decode(creds_bundle))
            self.aws_session = self._init_aws_session(**creds)
        else:
            self.aws_session = self._init_aws_session(profile_name=profile)
        self.service = self._init_connection(region_name)
        return

    def _init_aws_session(
        self,
        **kwargs,
    ) -> boto3.session.Session:
        return boto3.session.Session(**kwargs)

    def _init_connection(self, region: Optional[str]):
        if region is not None:
            return self.aws_session.client(
                self.service_name, config=Config(region_name=region)
            )
        return self.aws_session.client(self.service_name)
