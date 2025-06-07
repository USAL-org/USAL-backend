WITH
    question := <optional str>$question,
    qa_type:= <optional QAType>$type,

FILTERED_QA := (
    SELECT QASection
    FILTER (
    (.question ILIKE '%' ++ question ++ '%' IF EXISTS question ELSE TRUE)
    )
    AND .type = qa_type IF EXISTS qa_type ELSE TRUE
    ORDER BY .question ASC
    OFFSET <optional int64>$offset
    LIMIT <optional int64>$limit
)
SELECT FILTERED_QA {
    id,
    question,
    answer,
    status,
    type,
}