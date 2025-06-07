WITH
    search := <optional str>$search,

FILTERED_UNIVERSITY := (
    SELECT University
    FILTER (
    (.name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    ORDER BY .name ASC
    OFFSET <optional int64>$offset
    LIMIT <optional int64>$limit
)
SELECT FILTERED_UNIVERSITY {
    id,
    name,
    location,
    image,
    state:{
        id,
        name,
    },
    description,
    acceptance_rate,
    annual_fee,
    student_faculty_ratio,
    available_majors:{
        id,
        name,
    },
    admission_requirements,
    status,
    view_count,
}