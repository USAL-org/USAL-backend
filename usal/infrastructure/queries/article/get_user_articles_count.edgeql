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
)
SELECT {
    total_count := count(FILTERED_ARTICLE)
}
