SELECT Article {
    id,
    created_at,
    title,
    cover_image,
    duration,
    media,
    content,
    category:{
        id,
        name
    },
    author: {
        id,
        full_name,
        email,
        pp_url,
        short_description,
        description,
        social_links
    }
}
FILTER .id = <uuid>$article_id