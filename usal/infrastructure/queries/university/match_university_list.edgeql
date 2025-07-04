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
    degree :{
        id,
        name,
    },
    url,
    rating, 
    admission_requirements,
}