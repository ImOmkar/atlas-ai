
from enum import Enum


class ComplianceStatus(str, Enum):

    COMPLIANT = "COMPLIANT"

    PARTIALLY_COMPLIANT = (
        "PARTIALLY_COMPLIANT"
    )

    NON_COMPLIANT = "NON_COMPLIANT"

    NOT_ADDRESSED = "NOT_ADDRESSED"