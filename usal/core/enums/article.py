from enum import Enum


class ArticleType(Enum):
    NEWS = "news"
    BLOG = "blog"


class ArticleStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
