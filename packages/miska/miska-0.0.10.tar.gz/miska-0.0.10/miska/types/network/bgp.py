import contextlib
import typing as t


# class Community:
#     def __init__(self, value: int):  # ???
#         ...
#
#     @classmethod
#     def from_string(cls, val: str):
#         ...


class ASN:

    """BGP ASN data type

    https://networklessons.com/bgp/bgp-4-byte-number
    """

    _SEP = "."
    _ZERO = 0
    _TWO_BYTES = 2 ** 16
    _FOUR_BYTES = 2 ** 32

    def __init__(self, number: int):
        if not isinstance(number, int):
            raise TypeError(f"int expected, got: {type(number)}")

        if not (self._ZERO <= number < self._FOUR_BYTES):
            msg = f"Value must be in range {self._ZERO}-{self._FOUR_BYTES - 1}"
            raise ValueError(msg)

        self._number = number

    @classmethod
    def from_plain(cls, string: str) -> t.Self:
        if not isinstance(string, str):
            raise TypeError(f"str expected, got: {type(string)}")

        return cls(int(string))

    def to_plain(self) -> str:
        return str(self._number)

    @classmethod
    def from_asdot(cls, string: str) -> t.Self:
        with contextlib.suppress(Exception):
            result = cls.from_plain(string)
            if int(result) < cls._TWO_BYTES:
                return result
        return cls.from_asdotplus(string)

    def to_asdot(self) -> str:
        if self._number < self._TWO_BYTES:
            return self.to_plain()
        return self.to_asdotplus()

    @classmethod
    def from_asdotplus(cls, string: str) -> t.Self:
        if not isinstance(string, str):
            raise TypeError(f"str expected, got: {type(string)}")

        high, low = map(int, string.split(cls._SEP, maxsplit=1))
        return cls(high * cls._TWO_BYTES + low)

    def to_asdotplus(self) -> str:
        return self._SEP.join(map(str, divmod(self._number, self._TWO_BYTES)))

    @classmethod
    def parse(cls, data: int | str) -> t.Self:
        with contextlib.suppress(Exception):
            return cls(t.cast(int, data))
        data = t.cast(str, data)
        with contextlib.suppress(Exception):
            return cls.from_plain(data)
        with contextlib.suppress(Exception):
            return cls.from_asdotplus(data)
        raise ValueError(f"Unable to parse data into {cls}")

    def __int__(self) -> int:
        return self._number

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.to_asdotplus()}>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"

    def __copy__(self):
        return type(self)(self._number)

    def __deepcopy__(self, memo: dict[int, t.Any]):
        _id = id(self)
        if _id not in memo:
            memo[_id] = type(self)(self._number)
        return memo[_id]

    def __reduce__(self) -> tuple[t.Any, ...]:
        return self.__class__, (self._number,)

    def __hash__(self) -> int:
        return hash(self._number)

    def __eq__(self, other) -> bool:
        return (isinstance(other, self.__class__)
                and (int(other) == self._number))


# print(ASN(6541))   # 0.6541
# print(ASN(54233))  # 0.54233
# print(ASN(544))    # 0.544
#
# print(ASN(65536))    # 1.0
# print(ASN(65537))    # 1.1
# print(ASN(65538))    # 1.2
