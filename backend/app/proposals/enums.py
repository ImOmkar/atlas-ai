
from enum import Enum


class ProposalStatus(
    str,
    Enum,
):

    PENDING = "pending"
    
    PROCESSING = "processing"

    READY = "ready"

    FAILED = "failed"