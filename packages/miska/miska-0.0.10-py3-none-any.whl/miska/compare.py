class Comparable:
    def __init__(self, obj, comp):
        self.obj = obj
        self.value = self._make_value(comp)
        self._hash = hash(self.value)

    def _make_value(self, comp):
        return comp(self.obj) if callable(comp) else comp

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            msg = f"Can't compare {self.__class__} with {other.__class__}"
            raise TypeError(msg)

        return self.value == other.value
