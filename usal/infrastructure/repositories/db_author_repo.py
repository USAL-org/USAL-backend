from typing import override

from usal.core.exceptions.api_exception import api_exception

from usal.domain.entities.author_entity import GetAuthorEntity, ListAuthorsEntity
from usal.domain.repositories.author_repo import AuthorRepo
from usal.infrastructure.queries.author import (
    create_author_async_edgeql,
    list_authors_async_edgeql,
)


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
    async def list_all_author(self) -> ListAuthorsEntity:
        async with self.session() as session:
            db_author = await list_authors_async_edgeql.list_authors(session)
            return ListAuthorsEntity(
                records=[
                    GetAuthorEntity.model_validate(author, from_attributes=True)
                    for author in db_author
                ],
            )
