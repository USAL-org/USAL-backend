SELECT Article {
    id,
    title,
    cover_image,
    author: {
        id,
        full_name,
        pp_url
    }
}
FILTER .type = <ArticleType>$type