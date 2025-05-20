from fastapi import APIRouter
from usal.api.v1.admin_router import AdminRouter
from usal.api.v1.article_router import ArticleRouter


routers: list[APIRouter] = [
    ArticleRouter,
    AdminRouter,
]
