INSERT Author{
    full_name := <str>$full_name,
    email:= <str>$email,
    pp_url := <optional str>$pp_url,
    short_description := <str>$short_description,
    description := <optional str>$description,
    social_links := (
        IF EXISTS <optional array<str>>$social_links AND len(<optional array<str>>$social_links) > 0
        THEN array_unpack(<optional array<str>>$social_links) 
        ELSE {}
    ),
}