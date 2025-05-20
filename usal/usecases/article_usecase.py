from uuid import UUID

from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.domain.entities.article_entity import (
    ListArticleCategoriesEntity,
    ListArticlesEntity,
    ViewArticleDetailsEntity,
)
from usal.domain.repositories.article_repo import ArticleRepo


class ArticleUsecase:
    def __init__(
        self,
        repo: ArticleRepo,
    ) -> None:
        self.repo = repo

    async def create_article(
        self,
        request: CreateArticleRequest,
    ) -> None:
        return await self.repo.create_article(
            title=request.title,
            cover_image=request.cover_image,
            content=request.content,
            type=request.type,
            author=request.author,
            category=request.category,
            status=request.status,
            duration=request.duration,
            media=request.media,
        )

    async def list_all_articles(
        self,
        filter: ArticleFilterRequest,
    ) -> ListArticlesEntity:
        return await self.repo.list_all_articles(type=filter.type)

    async def create_article_category(
        self,
        request: CreateArticleCategoryRequest,
    ) -> None:
        return await self.repo.create_article_category(
            name=request.name,
        )

    async def list_all_article_categories(
        self,
    ) -> ListArticleCategoriesEntity:
        return await self.repo.list_all_article_categories()

    async def list_user_articles(
        self,
        filter: ArticleFilterRequest,
    ) -> ListArticlesEntity:
        return await self.repo.list_user_articles(type=filter.type)

    async def get_article_by_id(
        self,
        article_id: UUID,
    ) -> ViewArticleDetailsEntity:
        return await self.repo.get_article_by_id(article_id=article_id)

    # async def update_notification(
    #     self,
    #     notification_id: UUID,
    #     request: UpdateNotificationRequest,
    #     payload: JWTPayload,
    # ) -> BaseNotificationEntity:
    #     db_notification = await self.repo.get_notification_by_id(
    #         notification_id=notification_id
    #     )
    #     notification_obj = await self.repo.update_notification(
    #         notification_id=notification_id,
    #         title=request.title or db_notification.title,
    #         message=request.message or db_notification.message,
    #         send_to=request.send_to or db_notification.receiver,
    #         delivery_type=request.delivery_type or db_notification.delivery_type,
    #     )
    #     try:
    #         await self.activity_log_repo.create_activity_log(
    #             action=ActivityLogActions.UPDATED,
    #             row_id=str(notification_obj.id),
    #             table_name="Notification",
    #             admin_id=payload.admin_id,
    #             description="Notification Updated",
    #             changes=json.dumps(
    #                 {
    #                     "old_values": {"data": db_notification},
    #                     "new_values": {"data": request},
    #                 }
    #             ),
    #         )
    #     except Exception:
    #         raise api_exception(message="Failed to create activity log.")
    #     return notification_obj

    # async def delete_notification(
    #     self,
    #     notification_id: UUID,
    #     payload: JWTPayload,
    # ) -> BaseNotificationEntity:
    #     notification_obj = await self.repo.delete_notification(
    #         notification_id=notification_id
    #     )
    #     try:
    #         await self.activity_log_repo.create_activity_log(
    #             action=ActivityLogActions.DELETED,
    #             row_id=str(notification_obj.id),
    #             table_name="Notification",
    #             admin_id=payload.admin_id,
    #             description="Notification Deleted",
    #         )
    #     except Exception:
    #         raise api_exception(message="Failed to create activity log.")
    #     return notification_obj
