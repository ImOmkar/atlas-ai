
from enum import Enum


class ProposalStatus(
    str,
    Enum,
):

    PROCESSING = "processing"

    READY = "ready"

    FAILED = "failed"