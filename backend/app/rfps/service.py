# from sqlalchemy.orm import Session

# from app.documents.enums import DocumentStatus
# from app.documents.repository import DocumentRepository
# from app.projects.repository import ProjectRepository

# from app.rfps.enums import RFPStatus
# from app.rfps.models import RFP
# from app.rfps.repository import RFPRepository


# class RFPService:

#     def __init__(
#         self,
#         db: Session,
#     ):

#         self.project_repository = (
#             ProjectRepository(db)
#         )

#         self.document_repository = (
#             DocumentRepository(db)
#         )

#         self.repository = (
#             RFPRepository(db)
#         )

#     def create(
#         self,
#         organization_id: int,
#         project_id: int,
#         document_id: int,
#     ) -> RFP:

#         project = (
#             self.project_repository.get_by_id(
#                 organization_id,
#                 project_id,
#             )
#         )

#         if project is None:

#             raise ValueError(
#                 "Project not found."
#             )

#         document = (
#             self.document_repository.get_by_id(
#                 project_id,
#                 document_id,
#             )
#         )

#         if document is None:

#             raise ValueError(
#                 "Document not found."
#             )

#         if document.status != DocumentStatus.READY:

#             raise ValueError(
#                 "Document is not ready for RFP processing."
#             )

#         existing = (
#             self.repository.get_by_document_id(
#                 project_id,
#                 document_id,
#             )
#         )

#         if existing is not None:

#             return existing

#         rfp = RFP(
#             project_id=project_id,
#             document_id=document_id,
#             status=RFPStatus.PROCESSING,
#         )

#         return self.repository.create(
#             rfp,
#         )


from sqlalchemy.orm import Session

from app.rfps.models import RFP
from app.rfps.enums import RFPStatus

from app.rfps.repository import (
    RFPRepository,
)

from app.rfps.models import (
    RFPRequirement,
)

from app.rfp_requirements.repository import (
    RFPRequirementRepository,
)

from app.rfps.generator import (
    RFPGenerator,
)

from app.documents.repository import (
    DocumentRepository,
)

from app.document_chunks.repository import (
    DocumentChunkRepository,
)
from app.documents.enums import DocumentStatus


class RFPService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.rfp_repository = (
            RFPRepository(db)
        )

        self.requirement_repository = (
            RFPRequirementRepository(db)
        )

        self.document_repository = (
            DocumentRepository(db)
        )

        self.chunk_repository = (
            DocumentChunkRepository(db)
        )

        self.generator = (
            RFPGenerator()
        )


    def get(
        self,
        project_id: int,
        rfp_id: int,
    ):

        rfp = (
            self.rfp_repository.get_by_id(
                project_id,
                rfp_id,
            )
        )

        if rfp is None:
            raise ValueError(
                "RFP not found."
            )

        requirement = (
            self.requirement_repository.get_by_rfp_id(
                rfp.id,
            )
        )

        return (
            rfp,
            requirement,
        )

    def create_from_document(
        self,
        project_id: int,
        document_id: int,
    ) -> RFP:

        document = (
            self.document_repository.get_by_id(
                project_id,
                document_id,
            )
        )

        print(document)

        if document is None:
            raise ValueError(
                "Document not found."
            )

        if document.status != DocumentStatus.READY:
            raise ValueError(
                "Document is not ready for RFP extraction."
            )

        rfp = RFP(
            project_id=project_id,
            document_id=document_id,
            status=RFPStatus.PROCESSING,
        )

        rfp = self.rfp_repository.create(
            rfp
        )

        try:

            chunks = (
                self.chunk_repository.get_document_chunks(
                    document_id,
                )
            )

            if not chunks:
                raise ValueError(
                    "No document chunks found."
                )

            document_text = "\n\n".join(
                chunk.content
                for chunk in chunks
            )

            extracted = (
                self.generator.generate(
                    document_text,
                )
            )

            requirement = (
                RFPRequirement(
                    rfp_id=rfp.id,
                    title=extracted.get(
                        "title"
                    ),
                    client=extracted.get(
                        "client"
                    ),
                    submission_deadline=extracted.get(
                        "submission_deadline"
                    ),
                    project_overview=extracted.get(
                        "project_overview"
                    ),
                    mandatory_requirements=extracted.get(
                        "mandatory_requirements",
                        [],
                    ),
                    technical_requirements=extracted.get(
                        "technical_requirements",
                        [],
                    ),
                    functional_requirements=extracted.get(
                        "functional_requirements",
                        [],
                    ),
                    deliverables=extracted.get(
                        "deliverables",
                        [],
                    ),
                    evaluation_criteria=extracted.get(
                        "evaluation_criteria",
                        [],
                    ),
                    commercial_requirements=extracted.get(
                        "commercial_requirements",
                        [],
                    ),
                    eligibility_requirements=extracted.get(
                        "eligibility_requirements",
                        [],
                    ),
                )
            )

            self.requirement_repository.create(
                requirement
            )

            rfp.status = (
                RFPStatus.READY
            )

            self.db.commit()

            self.db.refresh(
                rfp
            )

            return rfp

        except Exception:

            self.db.rollback()

            rfp.status = (
                RFPStatus.FAILED
            )

            self.db.commit()

            self.db.refresh(
                rfp
            )

            raise