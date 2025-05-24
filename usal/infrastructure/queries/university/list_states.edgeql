WITH
    search := <optional str>$search,

SELECT State {
    id,
    name,
    country,
}
FILTER (
(.name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
)