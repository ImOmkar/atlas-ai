

from app.db.session import SessionLocal

from app.document_chunks.repository import (
    DocumentChunkRepository,
)

from app.proposals.requirement_service import (
    ProposalRequirementService,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        document_id = 23
        proposal_id = 6

        chunk_repository = (
            DocumentChunkRepository(db)
        )

        chunks = (
            chunk_repository.get_document_chunks(
                document_id,
            )
        )

        print(
            f"Loaded {len(chunks)} chunks."
        )

        document = "\n".join(
            chunk.content
            for chunk in chunks
        )

        service = (
            ProposalRequirementService(db)
        )

        requirement = (
            service.extract_and_save(
                proposal_id=proposal_id,
                document=document,
            )
        )

        print(
            "\nPROPOSAL REQUIREMENT SAVED:"
        )

        print(
            "Requirement ID:",
            requirement.id,
        )

        print(
            "Proposal ID:",
            requirement.proposal_id,
        )

        print(
            "Executive Summary:",
            requirement.executive_summary,
        )

        print(
            "Company Profile:",
            requirement.company_profile,
        )

        print(
            "Project Team:",
            requirement.project_team,
        )

        print(
            "Deliverables:",
            requirement.deliverables,
        )

        print(
            "Commercial Proposal:",
            requirement.commercial_proposal,
        )

    finally:

        db.close()