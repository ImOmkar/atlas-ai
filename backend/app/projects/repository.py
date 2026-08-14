from sqlalchemy.orm import Session

from app.projects.models import Project


class ProjectRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def get_by_id(
        self,
        organization_id: int,
        project_id: int,
    ) -> Project | None:
        return (
            self.db.query(Project)
            .filter(
                Project.id == project_id,
                Project.organization_id == organization_id,
            )
            .first()
        )

    def get_all(
        self,
        organization_id: int,
    ) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(
                Project.organization_id == organization_id,
            )
            .order_by(Project.created_at.desc())
            .all()
        )

    def create(
        self,
        project: Project,
    ) -> Project:

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project


    def update(
        self,
        project: Project,
    ) -> Project:

        self.db.commit()
        self.db.refresh(project)

        return project

    def delete(
        self,
        project: Project,
    ) -> None:
        self.db.delete(project)
        self.db.commit()