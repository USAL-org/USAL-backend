from enum import Enum


class ArticleType(Enum):
    NEWS = "NEWS"
    BLOG = "BLOG"


class ArticleStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
