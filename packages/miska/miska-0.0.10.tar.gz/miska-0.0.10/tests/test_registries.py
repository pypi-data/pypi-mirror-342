from miska import registries


def test_registry():
    class Registry(registries.RegistriesMixin):
        __registry_locator__ = "MY_TYPE"

    class MyDriver(Registry):
        MY_TYPE = "mine!"

    result = Registry.get_subclass_for("mine!")

    assert result == MyDriver
