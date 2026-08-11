

from app.db.session import SessionLocal

from app.db import models

from app.proposals.analysis.models import (
    ProposalAnalysis,
)

from app.proposals.analysis.repository import (
    ProposalAnalysisRepository,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = (
            ProposalAnalysisRepository(db)
        )

        analysis = ProposalAnalysis(
            proposal_id=6,
            overall_score=85.0,
            summary=(
                "Initial compliance analysis."
            ),
        )

        analysis = repository.create(
            analysis,
        )

        print(
            "Analysis ID:",
            analysis.id,
        )

        print(
            "Proposal ID:",
            analysis.proposal_id,
        )

        print(
            "Score:",
            analysis.overall_score,
        )

    finally:

        db.close()