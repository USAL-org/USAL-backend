from usal.api.schema.request.author_request import (
    CreateAuthorRequest,
    FilterAuthorRequest,
)
from usal.domain.entities.author_entity import GetAuthorEntity, ListAuthorsEntity
from usal.domain.repositories.author_repo import AuthorRepo


class AuthorUsecase:
    def __init__(
        self,
        repo: AuthorRepo,
    ) -> None:
        self.repo = repo

    async def create_author(
        self,
        request: CreateAuthorRequest,
    ) -> None:
        return await self.repo.create_author(
            full_name=request.full_name,
            email=request.email,
            short_description=request.short_description,
            pp_url=request.pp_url,
            description=request.description,
            social_links=request.social_links,
        )

    async def list_all_author(
        self,
        filter: FilterAuthorRequest,
    ) -> ListAuthorsEntity:
        author_obj = await self.repo.list_all_author(
            page=filter.page,
            limit=filter.limit,
            search=filter.search,
        )
        result = [
            GetAuthorEntity.model_validate(author, from_attributes=True)
            for author in author_obj.records
        ]
        return ListAuthorsEntity(
            page_info=author_obj.page_info,
            records=result,
        )
