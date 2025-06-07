SELECT (
  INSERT OTP {
    user := (
      SELECT User
      FILTER .id = <uuid>$user_id
    ),
    secret := <str>$secret,
    expiration_time := <datetime>$expiration_time
  }
) {
  id,
  user_id := .user.id,
  secret,
  expiration_time
}
