from app.db.session import SessionLocal

# Import related models so SQLAlchemy knows their tables.
from app.documents.models import Document
from app.projects.models import Project
from app.rfps.models import RFP

from app.rfps.repository import RFPRepository


if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = RFPRepository(
            db,
        )

        rfp = RFP(
            project_id=1,
            document_id=17,
        )

        repository.create(
            rfp,
        )

        print(
            "RFP ID:",
            rfp.id,
        )

        print(
            "RFP Status:",
            rfp.status,
        )

    finally:

        db.close()