
from app.documents.enums import DocumentStatus
from app.documents.repository import (
    DocumentRepository,
)

from app.rfps.repository import (
    RFPRepository,
)

from app.proposals.enums import (
    ProposalStatus,
)

from app.proposals.models import (
    Proposal,
)

from app.proposals.repository import (
    ProposalRepository,
)

from app.proposals.requirement_service import (
    ProposalRequirementService,
)

from app.document_chunks.repository import (
    DocumentChunkRepository,
)

from app.proposals.analysis.service import (
    ProposalAnalysisService,
)

from app.proposals.requirement_repository import (
    ProposalRequirementRepository,
)

from app.proposals.analysis.repository import (
    ProposalAnalysisRepository,
)

from app.proposals.analysis.compliance_repository import (
    ProposalComplianceItemRepository,
)

from app.proposals.schemas import (
    ProposalDetailsResponse,
)

class ProposalService:

    def __init__(self, db):

        self.db = db

        self.proposal_repository = (
            ProposalRepository(db)
        )

        self.rfp_repository = (
            RFPRepository(db)
        )

        self.document_repository = (
            DocumentRepository(db)
        )

        self.requirement_service = (
            ProposalRequirementService(db)
        )

        self.chunk_repository = (
            DocumentChunkRepository(db)
        )

        self.analysis_service = (
            ProposalAnalysisService(db)
        )

        self.requirement_repository = (
            ProposalRequirementRepository(db)
        )

        self.analysis_repository = (
            ProposalAnalysisRepository(db)
        )

        self.compliance_repository = (
            ProposalComplianceItemRepository(db)
        )

    def get_details(
        self,
        project_id: int,
        proposal_id: int,
    ) -> ProposalDetailsResponse:
        
        proposal = (
            self.proposal_repository.get_by_id(
                project_id=project_id,
                proposal_id=proposal_id,
            )
        )

        if proposal is None:
            raise ValueError(
                "Proposal not found."
            )

        requirement = (
            self.requirement_repository
            .get_by_proposal_id(
                proposal_id,
            )
        )

        analyses = (
            self.analysis_repository
            .get_all(
                proposal_id,
            )
        )

        analysis = (
            analyses[0]
            if analyses
            else None
        )

        compliance_items = []

        if analysis:

            compliance_items = (
                self.compliance_repository
                .get_by_analysis_id(
                    analysis.id,
                )
            )

        return ProposalDetailsResponse(
            id=proposal.id,
            project_id=proposal.project_id,
            rfp_id=proposal.rfp_id,
            document_id=proposal.document_id,
            status=proposal.status,
            requirements=requirement,
            analysis=analysis,
            compliance_items=compliance_items,
        )


    def get_by_id(
        self,
        project_id: int,
        proposal_id: int,
    ) -> Proposal | None:

        return (
            self.proposal_repository.get_by_id(
                project_id=project_id,
                proposal_id=proposal_id,
            )
        )

    def create_from_document(
        self,
        project_id: int,
        rfp_id: int,
        document_id: int,
    ) -> Proposal:

        rfp = (
            self.rfp_repository.get_by_id(
                project_id=project_id,
                rfp_id=rfp_id,
            )
        )

        if rfp is None:

            raise ValueError(
                "RFP not found."
            )

        document = (
            self.document_repository.get_by_id(
                project_id=project_id,
                document_id=document_id,
            )
        )

        if document is None:

            raise ValueError(
                "Document not found."
            )

        if document.status != DocumentStatus.READY:

            raise ValueError(
                "Document is not ready for proposal processing."
            )

        proposal = Proposal(
            project_id=project_id,
            rfp_id=rfp_id,
            document_id=document_id,
            status=ProposalStatus.PROCESSING,
        )

        proposal = (
            self.proposal_repository.create(
                proposal,
            )
        )

        return proposal


    def process(
        self,
        proposal: Proposal,
    ) -> Proposal:

        try:

            chunks = (
                self.chunk_repository
                .get_document_chunks(
                    proposal.document_id,
                )
            )

            if not chunks:

                raise ValueError(
                    "No document chunks found."
                )

            document = "\n".join(
                chunk.content
                for chunk in chunks
            )

            # Step 1:
            # Extract proposal requirements
            self.requirement_service.extract_and_save(
                proposal_id=proposal.id,
                document=document,
            )

            # Step 2:
            # Analyze proposal against RFP
            self.analysis_service.analyze_and_save(
                rfp_id=proposal.rfp_id,
                proposal_id=proposal.id,
            )

            # Step 3:
            # Everything succeeded
            proposal.status = (
                ProposalStatus.READY
            )

            self.proposal_repository.update(
                proposal,
            )

            self.db.commit()

            return proposal

        except Exception:

            self.db.rollback()

            proposal.status = (
                ProposalStatus.FAILED
            )

            self.proposal_repository.update(
                proposal,
            )

            self.db.commit()

            raise



  