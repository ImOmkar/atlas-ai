from slugify import slugify

from app.organizations.exceptions import OrganizationNotFoundError
from app.organizations.repository import OrganizationRepository

from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.exceptions import ProjectNotFoundError
from app.projects.schemas import UpdateProjectRequest


class ProjectService:

    def __init__(self, db):
        self.project_repository = ProjectRepository(db)
        self.organization_repository = OrganizationRepository(db)

    def get_by_id(
        self,
        organization_id: int,
        project_id: int,
    ) -> Project:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        return project
    

    def get_all(
        self,
        organization_id: int,
    ) -> list[Project]:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        return self.project_repository.get_all(
            organization_id,
        )

    def create(
        self,
        organization_id: int,
        request,
    ) -> Project:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        project = Project(
            organization_id=organization_id,
            name=request.name,
            slug=slugify(request.name),
            description=request.description,
        )

        return self.project_repository.create(
            project,
        )


    def update(
        self,
        organization_id: int,
        project_id: int,
        request: UpdateProjectRequest,
    ) -> Project:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        if request.name is not None:
            project.name = request.name
            project.slug = slugify(request.name)

        if request.description is not None:
            project.description = request.description

        return self.project_repository.update(
            project,
        )



    def delete(
        self,
        organization_id: int,
        project_id: int,
    ) -> None:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        self.project_repository.delete(
            project,
        )

