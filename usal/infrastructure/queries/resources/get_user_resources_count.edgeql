WITH
    search := <optional str>$search,

FILTERED_RESOURCES := (
    SELECT Resources
    FILTER (
    (.title ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    AND .status = ResourceStatus.ACTIVE
)
SELECT {
    total_count := count(FILTERED_RESOURCES)
}