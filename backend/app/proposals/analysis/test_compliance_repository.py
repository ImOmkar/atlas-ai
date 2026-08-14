

# from app.db.session import SessionLocal

# import app.db.models

# from app.proposals.analysis.enums import (
#     ComplianceStatus,
# )

# from app.proposals.analysis.models import (
#     ProposalComplianceItem,
# )

# from app.proposals.analysis.compliance_repository import (
#     ProposalComplianceItemRepository,
# )


# if __name__ == "__main__":

#     db = SessionLocal()

#     try:

#         repository = (
#             ProposalComplianceItemRepository(db)
#         )

#         item = ProposalComplianceItem(
#             analysis_id=1,

#             category="technical_requirements",

#             requirement=(
#                 "All API communication must use HTTPS/TLS."
#             ),

#             proposal_response=(
#                 "The proposed solution uses HTTPS/TLS "
#                 "for all API communication."
#             ),

#             status=ComplianceStatus.COMPLIANT,

#             evidence=(
#                 "The technical architecture section "
#                 "specifies HTTPS/TLS for API communication."
#             ),

#             remarks=(
#                 "The proposal satisfies this requirement."
#             ),
#         )

#         item = repository.create(
#             item,
#         )

#         print(
#             "Compliance Item ID:",
#             item.id,
#         )

#         print(
#             "Analysis ID:",
#             item.analysis_id,
#         )

#         print(
#             "Category:",
#             item.category,
#         )

#         print(
#             "Status:",
#             item.status,
#         )

#     finally:

#         db.close()


from app.db.session import SessionLocal

import app.db.models

from app.proposals.analysis.enums import (
    ComplianceStatus,
)

from app.proposals.analysis.models import (
    ProposalComplianceItem,
)

from app.proposals.analysis.compliance_repository import (
    ProposalComplianceItemRepository,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = (
            ProposalComplianceItemRepository(db)
        )

        # -------------------------
        # CREATE
        # -------------------------

        item = ProposalComplianceItem(
            analysis_id=1,

            category="technical_requirements",

            requirement=(
                "All API communication must use HTTPS/TLS."
            ),

            proposal_response=(
                "The proposed solution uses HTTPS/TLS "
                "for all API communication."
            ),

            status=ComplianceStatus.COMPLIANT,

            evidence=(
                "The technical architecture section "
                "specifies HTTPS/TLS for API communication."
            ),

            remarks=(
                "The proposal satisfies this requirement."
            ),
        )

        item = repository.create(item)

        print(
            "Created Item ID:",
            item.id,
        )

        print(
            "Created Analysis ID:",
            item.analysis_id,
        )

        print(
            "Created Status:",
            item.status,
        )

        # -------------------------
        # GET BY ID
        # -------------------------

        fetched_item = (
            repository.get_by_id(
                analysis_id=999,
                item_id=item.id,
            )
        )

        print(
            "Fetched Item ID:",
            fetched_item.id
            if fetched_item
            else None,
        )

        print(
            "Fetched Analysis ID:",
            fetched_item.analysis_id
            if fetched_item
            else None,
        )

        print(
            "Fetched Status:",
            fetched_item.status
            if fetched_item
            else None,
        )

    finally:

        db.close()