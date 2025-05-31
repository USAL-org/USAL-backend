SELECT EXISTS (
    SELECT User 
    FILTER .email = <str>$email and .status != UserStatus.INACTIVE and .status != UserStatus.DELETED
)