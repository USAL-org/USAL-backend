SELECT OTP {
    id,
    user_id := .user.id,
    secret,
    expiration_time
}
FILTER .id = <uuid>$verification_id