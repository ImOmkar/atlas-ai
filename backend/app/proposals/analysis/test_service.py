
from app.db.session import SessionLocal

from app.proposals.analysis.service import (
    ProposalAnalysisService,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        service = ProposalAnalysisService(db)

        result = service.analyze(
            rfp_id=5,
            proposal_id=6,
        )

        print(
            "\nANALYSIS RESULT:"
        )

        print(
            result,
        )

    finally:

        db.close()