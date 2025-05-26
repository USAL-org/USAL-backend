SELECT Admin {
  id,
  username,
  email,
  password:= .password_hash
}
FILTER .username = <str>$username
LIMIT 1;
