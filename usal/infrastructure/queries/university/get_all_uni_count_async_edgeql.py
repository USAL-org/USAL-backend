# AUTOGENERATED FROM 'usal/infrastructure/queries/university/get_all_uni_count.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import gel


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


@dataclasses.dataclass
class GetAllUniCountResult(NoPydanticValidation):
    total_count: int


async def get_all_uni_count(
    executor: gel.AsyncIOExecutor,
    *,
    search: str | None = None,
) -> GetAllUniCountResult:
    return await executor.query_single(
        """\
        WITH
            search := <optional str>$search,

        FILTERED_UNIVERSITY := (
            SELECT University
            FILTER (
            (.name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
            )
        )
        SELECT {
            total_count := count(FILTERED_UNIVERSITY)
        }\
        """,
        search=search,
    )
