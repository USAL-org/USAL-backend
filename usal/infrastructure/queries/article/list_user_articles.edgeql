WITH
    search := <optional str>$search,
    type:= <ArticleType>$type,

FILTERED_ARTICLE := (
    SELECT Article
    FILTER (
    (.title ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE) OR
    (.author.full_name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    AND .type = type
    AND .status = ArticleStatus.ACTIVE
    ORDER BY .title ASC
    OFFSET <optional int64>$offset
    LIMIT <optional int64>$limit
)
SELECT FILTERED_ARTICLE {
    id,
    title,
    cover_image,
    author: {
        id,
        full_name,
        pp_url
    }
}