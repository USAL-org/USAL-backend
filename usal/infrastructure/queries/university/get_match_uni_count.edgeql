WITH
    major := <uuid>$major,
    degree := <uuid>$degree,
    min_gpa := <float64>$min_gpa,
    test_required := <bool>$test_required,
    min_fee := <float64>$min_fee,
    max_fee := <float64>$max_fee,

FILTERED_UNIVERSITY := (
    SELECT University
    FILTER (.min_gpa <= min_gpa)
    AND (.annual_fee >= min_fee)
    AND (.annual_fee <= max_fee)
    AND (.test_required = test_required)
    AND (.available_majors.id = major)
    AND (.degree.id = degree)
    AND (.status = UniversityStatus.ACTIVE)
)
SELECT {
    total_count := count(FILTERED_UNIVERSITY)
}