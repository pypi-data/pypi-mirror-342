import collections
import itertools
import operator
import typing as t


class GroupByAttr:
    def __init__(self,
                 attr_name: str,
                 grouping_map: dict[str, t.Any],
                 default_group: str = "others"):
        self._attr_name = attr_name
        self._default_group = default_group
        self._grouping = dict(map(reversed, grouping_map.items()))
        self._key_func = operator.attrgetter(self._attr_name)

    def __call__(self, iterable):
        iterable = sorted(iterable, key=self._key_func)
        grouped = itertools.groupby(iterable, key=self._key_func)

        result = collections.defaultdict(list)
        for key_value, it in grouped:
            key = self._grouping.get(key_value, self._default_group)
            result[key].extend(it)

        return result


def interseq(ileft: t.Iterable,
             iright: t.Iterable,
             /, *,
             key: t.Callable[[t.Any], t.Hashable] = lambda item: item):
    left_map = {key(item): item for item in ileft}
    right_map = {key(item): item for item in iright}
    common_keys = set(left_map).intersection(right_map)
    left = tuple(v for k, v in left_map.items() if k not in common_keys)
    right = tuple(v for k, v in right_map.items() if k not in common_keys)
    common = tuple((left_map[key], right_map[key]) for key in common_keys)
    return left, common, right
