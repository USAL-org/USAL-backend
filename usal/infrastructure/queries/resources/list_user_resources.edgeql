WITH
    search := <optional str>$search,

FILTERED_RESOURCES := (
    SELECT Resources
    FILTER (
    (.title ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    AND .status = ResourceStatus.ACTIVE
    ORDER BY .title ASC
    OFFSET <optional int64>$offset
    LIMIT <optional int64>$limit
)
SELECT FILTERED_RESOURCES {
    id,
    title,
    image,
    description,
    file,
}