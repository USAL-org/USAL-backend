SELECT User{
    id,
    full_name,
    email,
    phone_number,
    password_hash,
    gender,
    verified,
    pp_url,
    date_of_birth,
}
FILTER .id = <uuid>$user_id
LIMIT 1