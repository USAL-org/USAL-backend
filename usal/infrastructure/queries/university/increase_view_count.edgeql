UPDATE University
FILTER .id = <uuid>$university_id
SET {
  view_count := .view_count + 1,
}
