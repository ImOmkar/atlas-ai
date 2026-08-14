
from enum import Enum


class RFPStatus(str, Enum):

    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"