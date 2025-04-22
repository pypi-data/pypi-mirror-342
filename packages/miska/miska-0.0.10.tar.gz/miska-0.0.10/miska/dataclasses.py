import dataclasses
import logging


# NOTE(d.burmistrov): this module is DEPRECATED
logging.getLogger(__name__).warning("Module `dataclasses` is deprecated in Miska")  # noqa


_K_PRIVATE = "private"
_K_METADATA = "metadata"
_BASE_MODEL_INIT_FLAG = "_BASE_MODEL_INIT_FLAG"


def public_field(**kwargs) -> dataclasses.Field:
    kwargs.setdefault(_K_METADATA, {})[_K_PRIVATE] = False
    return dataclasses.field(**kwargs)


def private_field(**kwargs) -> dataclasses.Field:
    kwargs.setdefault(_K_METADATA, {})[_K_PRIVATE] = True
    return dataclasses.field(**kwargs)


class BaseModel:

    """Base class for dataclass magic

    - supports private fields that can't be modified

    from dataclasses import *
    from miska.dataclasses import *

    @dataclass
    class MyDataClass(BaseModel):
        public_field: str = public_field()
        private_field: str = private_field()

    d = MyDataClass("a", "b")
    print(d)  # MyDataClass(public_field='a', private_field='b')

    d.public_field = "A"
    print(d)  # MyDataClass(public_field='A', private_field='b')

    d.private_field = "B"
    # AttributeError: Forbidden to modify private attribute: private_field
    """

    __allow_attribute_deletion__ = False
    __default_private__ = True

    __PRIVATES = {}

    as_tuple = dataclasses.astuple
    as_dict = dataclasses.asdict

    def __post_init__(self):
        self._validate()
        self._mark_init_finished()

    def _mark_init_finished(self) -> None:
        setattr(self, _BASE_MODEL_INIT_FLAG, False)

    def _setattr(self, key, value):
        return super().__setattr__(key, value)

    def _validate(self) -> None:
        pass

    def __discover_privates(self):
        privates = set()
        for field in dataclasses.fields(self):
            flag = field.metadata.get(_K_PRIVATE, self.__default_private__)
            if flag:
                privates.add(field.name)
        return privates

    def __get_privates(self):
        privates = self.__PRIVATES.get(self.__class__)
        if privates is None:
            privates = self.__discover_privates()
            self.__PRIVATES[self.__class__] = privates
        return privates

    def __setattr__(self, key: str, value):
        # allow to initialize instance during dataclass magic
        if getattr(self, _BASE_MODEL_INIT_FLAG, True):
            return super().__setattr__(key, value)
        # allow managing regular private attributes
        elif key.startswith("_") and hasattr(self, key):
            return super().__setattr__(key, value)

        privates = self.__get_privates()

        # magic for inner modification like `self._private_field = 42`
        #   (it converts name into field that marked as private)
        if key.startswith("_"):
            _key = key[1:]
            if _key in privates:
                return super().__setattr__(_key, value)

        # magic for restricting private field modifications
        if key in privates:
            msg = f"Forbidden to modify private attribute: {key}"
            raise AttributeError(msg)

        return super().__setattr__(key, value)

    def __delattr__(self, item):
        if self.__allow_attribute_deletion__:
            return super().__delattr__(item)

        raise AttributeError("Attributes can't be deleted")
