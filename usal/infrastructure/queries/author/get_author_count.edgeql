WITH
  search := <optional str>$search,

  FILTERED_AUTHOR := (
    SELECT Author
    FILTER (
    (.full_name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
  )

SELECT {
    total_count := count(FILTERED_AUTHOR)
}
