UPDATE User
FILTER .id = <uuid>$user_id
SET {
  password_hash := <str>$new_password,
}