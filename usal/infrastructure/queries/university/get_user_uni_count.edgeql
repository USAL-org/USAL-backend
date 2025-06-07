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
)
SELECT {
    total_count := count(FILTERED_UNIVERSITY)
}