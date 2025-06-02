from fastapi import APIRouter
from usal.api.v1.admin_auth_router import AdminAuthRouter
from usal.api.v1.admin_router import AdminRouter
from usal.api.v1.university_router import UniversityRouter
from usal.api.v1.user_router import UserRouter
from usal.api.v1.user_auth_router import UserAuthRouter

routers: list[APIRouter] = [
    UserAuthRouter,
    UserRouter,
    AdminAuthRouter,
    AdminRouter,
    UniversityRouter,
]
