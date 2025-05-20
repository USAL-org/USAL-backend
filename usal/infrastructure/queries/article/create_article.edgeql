INSERT Article{
    title := <str>$title,
    cover_image:= <str>$cover_image,
    duration := <optional str>$duration,
    media := (
        IF EXISTS <optional array<str>>$media AND len(<optional array<str>>$media) > 0
        THEN array_unpack(<optional array<str>>$media) 
        ELSE {}
    ),
    content := <str>$content,
    type := <ArticleType>$type,
    author:=(
        SELECT Author
        FILTER .id = <uuid>$author
    ),
    category:=(
        SELECT ArticleCategory
        FILTER .id = <uuid>$category
    ),
    status := <ArticleStatus>$status,
}