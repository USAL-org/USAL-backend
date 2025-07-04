INSERT University{
    name := <str>$name,
    location := <str>$location,
    image := <str>$image,
    application_fee := <bool>$application_fee,
    community_college := <bool>$community_college,
    state:=(
        SELECT State
        FILTER .id = <uuid>$state
    ),
    description := <str>$description,
    acceptance_rate := <str>$acceptance_rate,
    annual_fee := <str>$annual_fee,
    student_faculty_ratio := <str>$student_faculty_ratio,
    available_majors := DISTINCT((
        FOR id IN array_unpack(<array<uuid>>$available_majors)
        UNION (
            SELECT Major 
            FILTER .id = id
        )
    )),
    admission_requirements := (
        IF EXISTS <array<str>>$admission_requirements AND len(<array<str>>$admission_requirements) > 0
        THEN array_unpack(<array<str>>$admission_requirements) 
        ELSE {}
    ),
    status := <UniversityStatus>$status,
    degree := DISTINCT((
        FOR id IN array_unpack(<array<uuid>>$degrees)
        UNION (
            SELECT Degree 
            FILTER .id = id
        )
    )),
    url := <str>$url,
    rating := <float64>$rating,
    featured := <bool>$featured,
}