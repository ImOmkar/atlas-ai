
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
from app.proposals.analysis.enums import ComplianceStatus
from app.proposals.exceptions import ProposalProcessingError

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


    def get_analysis(
        self,
        project_id: int,
        proposal_id: int,
    ):
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

        analysis = (
            self.analysis_repository
            .get_all(
                proposal_id,
            )
        )

        if not analysis:
            raise ValueError(
                "Proposal analysis not found."
            )

        return analysis[0]


    def get_analysis_compliance(
        self,
        project_id: int,
        proposal_id: int,
        status: ComplianceStatus | None = None,
    ):
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

        analyses = (
            self.analysis_repository
            .get_all(
                proposal_id,
            )
        )

        if not analyses:
            raise ValueError(
                "Proposal analysis not found."
            )

        analysis = analyses[0]

        if status is None:

            return (
                self.compliance_repository
                .get_by_analysis_id(
                    analysis.id,
                )
            )

        return (
            self.compliance_repository
            .get_by_analysis_id_and_status(
                analysis_id=analysis.id,
                status=status,
            )
        )


    def get_analysis_summary(
        self,
        project_id: int,
        proposal_id: int,
    ):
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

        analyses = (
            self.analysis_repository.get_all(
                proposal_id,
            )
        )

        if not analyses:
            raise ValueError(
                "Proposal analysis not found."
            )

        analysis = analyses[0]

        compliance_items = (
            self.compliance_repository
            .get_by_analysis_id(
                analysis.id,
            )
        )

        total_requirements = len(
            compliance_items
        )

        compliant = 0
        partially_compliant = 0
        non_compliant = 0
        not_addressed = 0

        for item in compliance_items:

            if item.status == ComplianceStatus.COMPLIANT:
                compliant += 1

            elif (
                item.status
                == ComplianceStatus.PARTIALLY_COMPLIANT
            ):
                partially_compliant += 1

            elif (
                item.status
                == ComplianceStatus.NON_COMPLIANT
            ):
                non_compliant += 1

            elif (
                item.status
                == ComplianceStatus.NOT_ADDRESSED
            ):
                not_addressed += 1

        compliance_percentage = (
            (
                compliant
                + (partially_compliant * 0.5)
            )
            / total_requirements
            * 100
            if total_requirements
            else 0.0
        )

        return {
            "proposal_id": proposal.id,
            "analysis_id": analysis.id,
            "overall_score": analysis.overall_score,
            "total_requirements": total_requirements,
            "compliant": compliant,
            "partially_compliant": (
                partially_compliant
            ),
            "non_compliant": non_compliant,
            "not_addressed": not_addressed,
            "compliance_percentage": round(
                compliance_percentage,
                2,
            ),
            "summary": analysis.summary,
        }


    def get_compliance_items_paginated(
        self,
        project_id: int,
        proposal_id: int,
        page: int,
        page_size: int,
        status: ComplianceStatus | None = None,
    ):
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

        analyses = (
            self.analysis_repository.get_all(
                proposal_id,
            )
        )

        if not analyses:
            raise ValueError(
                "Proposal analysis not found."
            )

        analysis = analyses[0]

        items, total = (
            self.compliance_repository
            .get_by_analysis_id_paginated(
                analysis_id=analysis.id,
                page=page,
                page_size=page_size,
                status=status,
            )
        )

        total_pages = (
            (total + page_size - 1)
            // page_size
            if total
            else 0
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

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
            status=ProposalStatus.PENDING,
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

        if proposal.status == ProposalStatus.READY:

            raise ProposalProcessingError(
                "Proposal has already been processed."
            )

        if proposal.status == ProposalStatus.PROCESSING:

            raise ProposalProcessingError(
                "Proposal is already being processed."
            )

        if proposal.status == ProposalStatus.PENDING:

            proposal.status = ProposalStatus.PROCESSING

            self.proposal_repository.update(
                proposal,
            )

            self.db.commit()

        try:

            chunks = (
                self.chunk_repository
                .get_document_chunks(
                    proposal.document_id,
                )
            )

            if not chunks:

                raise ProposalProcessingError(
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

            # raise ValueError(
            #     "TEST: intentional analysis failure"
            # )

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

        except Exception as e:

            print(
                "\nPROCESSING ERROR:",
                repr(e),
            )

            self.db.rollback()

            proposal.status = (
                ProposalStatus.FAILED
            )

            self.proposal_repository.update(
                proposal,
            )

            self.db.commit()

            raise



  