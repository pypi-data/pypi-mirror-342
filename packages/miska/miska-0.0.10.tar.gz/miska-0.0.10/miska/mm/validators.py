from marshmallow import validate


class Lambda(validate.Validator):
    def __init__(self, func):
        self.func = func

    def __call__(self, value):
        if self.func(value):
            return value

        raise validate.ValidationError("Lambda failed")


class HasKeys(validate.Validator):
    def __init__(self, *keys):
        self.keys = set(keys)

    def __call__(self, value):
        if self.keys.issubset(value):
            return value

        msg = f"Missing keys: {', '.join(self.keys)}"
        raise validate.ValidationError(msg)
