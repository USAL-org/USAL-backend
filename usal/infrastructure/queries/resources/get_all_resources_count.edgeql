WITH
    search := <optional str>$search,

FILTERED_RESOURCES := (
    SELECT Resources
    FILTER (
    (.title ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    OFFSET <optional int64>$offset
    LIMIT <optional int64>$limit
)
SELECT {
    total_count := count(FILTERED_RESOURCES)
}