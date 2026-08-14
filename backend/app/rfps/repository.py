

from sqlalchemy.orm import Session

from app.rfps.models import RFP
from app.db.session import SessionLocal


class RFPRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def create(
        self,
        rfp: RFP,
    ) -> RFP:

        self.db.add(
            rfp,
        )

        self.db.commit()

        self.db.refresh(
            rfp,
        )

        return rfp

    def get_by_id(
        self,
        project_id: int,
        rfp_id: int,
    ) -> RFP | None:

        return (
            self.db.query(RFP)
            .filter(
                RFP.id == rfp_id,
                RFP.project_id == project_id,
            )
            .first()
        )

    def get_by_document_id(
        self,
        project_id: int,
        document_id: int,
    ) -> RFP | None:

        return (
            self.db.query(RFP)
            .filter(
                RFP.project_id == project_id,
                RFP.document_id == document_id,
            )
            .first()
        )

    def get_all(
        self,
        project_id: int,
    ) -> list[RFP]:

        return (
            self.db.query(RFP)
            .filter(
                RFP.project_id == project_id,
            )
            .order_by(
                RFP.created_at.desc(),
            )
            .all()
        )

    def update(
        self,
        rfp: RFP,
    ) -> RFP:

        self.db.commit()

        self.db.refresh(
            rfp,
        )

        return rfp

    def delete(
        self,
        rfp: RFP,
    ) -> None:

        self.db.delete(
            rfp,
        )

        self.db.commit()



# if __name__ == "__main__":

#     db = SessionLocal()

#     repository = RFPRepository(db)

#     rfp = RFP(
#         project_id=1,
#         document_id=17,
#     )

#     repository.create(rfp)

#     print(rfp.id)
#     print(rfp.status)


