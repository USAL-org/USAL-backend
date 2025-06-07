WITH
    question := <optional str>$question,
    qa_type:= <QAType>$type,

FILTERED_QA := (
    SELECT QASection
    FILTER (
    (.question ILIKE '%' ++ question ++ '%' IF EXISTS question ELSE TRUE)
    )
    AND .type = qa_type
    AND .status = QAStatus.ACTIVE
)
SELECT {
    total_count := count(FILTERED_QA)
}