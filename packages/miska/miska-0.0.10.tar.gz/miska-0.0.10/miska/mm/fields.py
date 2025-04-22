import types

import marshmallow as mm
from marshmallow import exceptions as excs
from marshmallow import utils


def _wrap(wrap_type):
    def decorator(func):
        return lambda *args, **kwargs: wrap_type(func(*args, **kwargs))

    return decorator


class MappingProxy(mm.fields.Dict):
    _serialize = _wrap(dict)(mm.fields.Dict._serialize)
    _deserialize = _wrap(types.MappingProxyType)(mm.fields.Dict._deserialize)


class TensileTuple(mm.fields.Field):
    #: Default error messages.
    default_error_messages = {"invalid": "Not a valid tuple."}

    def __init__(self, item_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            utils.resolve_field_instance(item_type)
        except excs.FieldInstanceResolutionError as exc:
            msg = ("Value of 'item_type' must be subclasses"
                   " or instances of marshmallow.base.FieldABC.")
            raise ValueError(msg) from exc
        self.item_type = item_type

    def _serialize(self, value, attr, obj, **kwargs) -> tuple | None:
        if value is None:
            return None

        return tuple(self.item_type._serialize(item, attr, obj, **kwargs)
                     for item in value)

    def _deserialize(self, value, attr, data, **kwargs) -> tuple:
        if not mm.utils.is_collection(value):
            raise self.make_error("invalid")

        result = []
        errors = {}
        for idx, item in enumerate(value):
            try:
                result.append(self.item_type.deserialize(item, **kwargs))
            except mm.ValidationError as error:
                if error.valid_data is None:
                    errors.update({idx: error.messages})
                else:
                    result.append(error.valid_data)
        if errors:
            raise mm.ValidationError(errors, valid_data=result)

        return tuple(result)
