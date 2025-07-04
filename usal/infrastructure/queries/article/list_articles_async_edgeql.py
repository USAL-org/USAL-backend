# AUTOGENERATED FROM 'usal/infrastructure/queries/article/list_articles.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import enum
import gel
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        _ = pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


class ArticleStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ArticleType(enum.Enum):
    NEWS = "NEWS"
    BLOG = "BLOG"


class ArticleType02(enum.Enum):
    NEWS = "NEWS"
    BLOG = "BLOG"


@dataclasses.dataclass
class ListArticlesResult(NoPydanticValidation):
    id: uuid.UUID
    title: str
    cover_image: str
    status: ArticleStatus
    type: ArticleType
    author: ListArticlesResultAuthor


@dataclasses.dataclass
class ListArticlesResultAuthor(NoPydanticValidation):
    id: uuid.UUID
    full_name: str
    pp_url: str | None


async def list_articles(
    executor: gel.AsyncIOExecutor,
    *,
    search: str | None = None,
    type: ArticleType02 | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> list[ListArticlesResult]:
    return await executor.query(
        """\
        WITH
            search := <optional str>$search,
            type:= <optional ArticleType>$type,

        FILTERED_ARTICLE := (
            SELECT Article
            FILTER (
            (.title ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE) OR
            (.author.full_name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
            )
            AND (.type = type IF EXISTS type ELSE TRUE)
            ORDER BY .created_at DESC
            OFFSET <optional int64>$offset
            LIMIT <optional int64>$limit
        )
        SELECT FILTERED_ARTICLE {
            id,
            title,
            cover_image,
            status,
            type,
            author: {
                id,
                full_name,
                pp_url
            }
        }\
        """,
        search=search,
        type=type,
        offset=offset,
        limit=limit,
    )
