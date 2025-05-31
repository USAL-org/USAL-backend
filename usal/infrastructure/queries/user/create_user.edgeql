SELECT(INSERT User{
    full_name := <str>$full_name,
    email := <str>$email,
    phone_number := <str>$phone_number,
    password_hash := <str>$password,
})
{
    id,
    full_name,
    email,
    phone_number,
    password_hash,
    verified,
}