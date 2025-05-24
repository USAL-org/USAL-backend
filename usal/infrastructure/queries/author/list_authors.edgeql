WITH
    search := <optional str>$search,

FILTERED_AUTHOR := (
    SELECT Author
    FILTER (
    (.full_name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    ORDER BY .full_name ASC
    OFFSET <optional int64>$offset
    LIMIT <optional int64>$limit
)
SELECT FILTERED_AUTHOR {
    id,
    full_name,
    pp_url
}