WITH
    search := <optional str>$search,

SELECT Major {
    id,
    name,
}
FILTER (
(.name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
)