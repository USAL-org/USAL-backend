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
}