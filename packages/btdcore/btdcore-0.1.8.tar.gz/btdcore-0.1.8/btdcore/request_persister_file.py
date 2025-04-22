import os
from pathlib import Path

from btdcore.rest_client_base import PersistableRequestMetadata, RequestPersister


class RequestPersisterFile(RequestPersister):
    def __init__(self, file_name: str):
        self.file_path = Path(file_name)
        Path(os.path.dirname(self.file_path)).mkdir(parents=True, exist_ok=True)
        return

    def persist(self, batch: list[PersistableRequestMetadata]):
        with open(self.file_path, "a") as f:
            for metadata in batch:
                f.write(metadata.to_json())
                f.write("\n")
                pass
            pass
        return

    pass
