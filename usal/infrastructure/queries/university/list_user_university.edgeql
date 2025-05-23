WITH
    search := <optional str>$search,
    state := <optional uuid>$state,
    major := <optional uuid>$major,
    application_fee := <optional bool>$application_fee,
    community_college := <optional bool>$community_college,

FILTERED_UNIVERSITY := (
    SELECT University
    FILTER (
    (.name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
    )
    AND (.state.id = state IF EXISTS state ELSE TRUE)
    AND (.available_majors.id = major IF EXISTS major ELSE TRUE)
    AND (.application_fee = application_fee IF EXISTS application_fee ELSE TRUE)
    AND (.community_college = community_college IF EXISTS community_college ELSE TRUE)
    AND (.status = UniversityStatus.ACTIVE)
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
}