SELECT AdminPermission{
    id,
    permission,
}
FILTER .admin.id =<uuid>$admin_id