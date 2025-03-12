import enum


class RoleCode(enum.Enum):

    ADMIN = "admin"
    CONSUMER = "consumer"
    ARTISAN = "artisan"


class AccountState(enum.Enum):
    TYPE = "account_state"

    ACTIVE = "active"
    INACTIVE = "inactive"
