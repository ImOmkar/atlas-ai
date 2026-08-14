

from app.db.session import SessionLocal

from app.proposals.analysis.service import (
    ProposalAnalysisService,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        service = ProposalAnalysisService(db)

        analysis = service.analyze_and_save(
            rfp_id=5,
            proposal_id=6,
        )

        print(
            "\nANALYSIS CREATED:"
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

        print(
            "Summary:",
            analysis.summary,
        )

        items = (
            service.compliance_repository
            .get_by_analysis_id(
                analysis.id,
            )
        )

        print(
            "Compliance Items:",
            len(items),
        )

    finally:

        db.close()