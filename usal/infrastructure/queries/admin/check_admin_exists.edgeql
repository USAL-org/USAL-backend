SELECT EXISTS (
    SELECT Admin
    FILTER .id = <uuid>$admin_id
)
