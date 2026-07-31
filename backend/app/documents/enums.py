from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADING = "uploading"
    READY = "ready"
    FAILED = "failed"