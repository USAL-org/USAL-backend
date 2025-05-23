WITH
    search := <optional str>$search,
    type:= <optional ArticleType>$type,

FILTERED_ARTICLE := (
    SELECT Article
    FILTER (
    (.title ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE) OR
    (.author.full_name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    AND (.type = type IF EXISTS type ELSE TRUE)
)
SELECT {
    total_count := count(FILTERED_ARTICLE)
}
