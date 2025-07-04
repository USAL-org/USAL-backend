# AUTOGENERATED FROM 'usal/infrastructure/queries/qa/get_all_qa_count.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import enum
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
class GetAllQaCountResult(NoPydanticValidation):
    total_count: int


class QAType(enum.Enum):
    UNIVERSITY = "UNIVERSITY"
    ACADEMIC = "ACADEMIC"
    FINANCIAL = "FINANCIAL"
    PERSONAL = "PERSONAL"
    GRADUATE = "GRADUATE"
    POST_GRADUATE = "POST_GRADUATE"
    PHD = "PHD"
    FAMILY = "FAMILY"


async def get_all_qa_count(
    executor: gel.AsyncIOExecutor,
    *,
    question: str | None = None,
    type: QAType | None = None,
) -> GetAllQaCountResult:
    return await executor.query_single(
        """\
        WITH
            question := <optional str>$question,
            qa_type:= <optional QAType>$type,

        FILTERED_QA := (
            SELECT QASection
            FILTER (
            (.question ILIKE '%' ++ question ++ '%' IF EXISTS question ELSE TRUE)
            )
            AND .type = qa_type IF EXISTS qa_type ELSE TRUE
        )
        SELECT {
            total_count := count(FILTERED_QA)
        }\
        """,
        question=question,
        type=type,
    )
