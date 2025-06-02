SELECT User{
    id,
    full_name,
    email,
    password_hash,
    verified,
}
FILTER .email = <str>$email
LIMIT 1