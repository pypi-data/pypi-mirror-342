import enum


class PreserveCaseStrEnum(enum.StrEnum):
    """Copy enum names into their values

    class StatusEnum(PreserveCaseStrEnum):
         ok = auto()       # StatusEnum.ok.value == "ok"
         FAILED = auto( )  # StatusEnum.FAILED.value == "FAILED"
         Unknown = auto()  # StatusEnum.Unknown.value == "Unknown"
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name


def member_on_missing(member_name):
    """Provide default member on missing

    class StatusEnum(str, enum.Enum):
         OK = 'ok'
         FAILED = 'failed'
         _missing_ = enums.member_on_missing("FAILED")

    StatusEnum.OK  # <StatusEnum.OK: 'ok'>
    StatusEnum.FAILED  # <StatusEnum.FAILED: 'failed'>

    StatusEnum("ok")  # <StatusEnum.OK: 'ok'>
    StatusEnum("failed")  # <StatusEnum.FAILED: 'failed'>

    # HOW IT WORKS
    StatusEnum("unknown")  # <StatusEnum.FAILED: 'failed'>
    """

    return classmethod(lambda cls, value: getattr(cls, member_name))
