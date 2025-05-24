from typing import override

from usal.core.exceptions.api_exception import api_exception

from usal.domain.entities.author_entity import GetAuthorEntity, ListAuthorsEntity
from usal.domain.repositories.author_repo import AuthorRepo
from usal.infrastructure.queries.author import (
    create_author_async_edgeql,
    get_author_count_async_edgeql,
    list_authors_async_edgeql,
)
from usal.infrastructure.repositories.pagination_repo import paginate


class DbAuthorRepo(AuthorRepo):
    @override
    async def create_author(
        self,
        full_name: str,
        email: str,
        short_description: str,
        pp_url: str | None = None,
        description: str | None = None,
        social_links: list[str] | None = None,
    ) -> None:
        async with self.session() as session:
            author_obj = await create_author_async_edgeql.create_author(
                session,
                full_name=full_name,
                email=email,
                short_description=short_description,
                pp_url=pp_url,
                description=description,
                social_links=social_links,
            )
            if not author_obj:
                raise api_exception(
                    message="Unable to create author. Please try again.",
                )

    @override
    async def list_all_author(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListAuthorsEntity:
        async with self.session() as session:
            total_count = await get_author_count_async_edgeql.get_author_count(
                session,
                search=search,
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_author = await list_authors_async_edgeql.list_authors(
                session,
                offset=page_info.offset,
                limit=limit,
                search=search,
            )
            return ListAuthorsEntity(
                page_info=page_info,
                records=[
                    GetAuthorEntity.model_validate(author, from_attributes=True)
                    for author in db_author
                ],
            )
