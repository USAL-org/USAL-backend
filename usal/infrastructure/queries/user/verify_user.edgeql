UPDATE User
FILTER .id = <uuid>$user_id
SET {
  verified := true,
}