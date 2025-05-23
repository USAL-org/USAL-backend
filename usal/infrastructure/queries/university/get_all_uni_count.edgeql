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
}