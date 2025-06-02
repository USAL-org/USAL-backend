from enum import Enum


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "OTHERS"


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"
