import types
import typing as t


class BaseRegistryError(Exception):
    pass


class SubclassMissingQualifier(BaseRegistryError):
    pass


class SubclassNotFound(BaseRegistryError):
    pass


class ClassRegistriesMixin:
    __registries: dict[str, dict[t.Any, type]] = {}

    __registry_type__: str  # default: class name
    __registry_qualifier__: str | t.Callable[[t.Type], str]

    @classmethod
    def __get_type(cls):
        return getattr(cls, "__registry_type__", cls.__name__)

    @classmethod
    def get_qualifier(cls):
        qualifier = getattr(cls, "__registry_qualifier__", None)
        if qualifier is None:
            raise SubclassMissingQualifier(cls)
        return qualifier

    @classmethod
    def get_identity(cls):
        qualifier = cls.get_qualifier()
        if isinstance(qualifier, str):
            identity = getattr(cls, qualifier, None)
        else:
            identity = qualifier(cls)

        return identity

    def __init_subclass__(cls, **kwargs: t.Any):
        super().__init_subclass__(**kwargs)
        mixin = ClassRegistriesMixin

        if mixin in cls.__bases__:
            cls.__registry_type__ = cls.__get_type()  # enrich
            cls.get_qualifier()  # validation
        else:
            store = mixin.__registries.setdefault(cls.__get_type(), {})
            store[cls.get_identity()] = cls

    @classmethod
    def get_subclass_for(cls, identity: t.Any) -> type:
        store = cls.__registries[cls.__registry_type__]
        if identity not in store:
            raise SubclassNotFound(identity)
        return store[identity]

    @classmethod
    def list_subclasses(cls) -> types.MappingProxyType[str, type]:
        store = cls.__registries[cls.__registry_type__]
        return types.MappingProxyType(store.copy())
