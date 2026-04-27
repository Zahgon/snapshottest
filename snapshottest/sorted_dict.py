from collections import OrderedDict


class SortedDict(OrderedDict):
    def __init__(self, values):
        super(SortedDict, self).__init__()

        try:
            sorted_items = sorted(values.items())
        except TypeError:
            # Enums are not sortable
            sorted_items = values.items()
        for key, value in sorted_items:
            if isinstance(value, dict):
                self[key] = SortedDict(value)
            elif isinstance(value, list):
                self[key] = self._sort_list(value)
            else:
                self[key] = value

    def _sort_list(self, value):
        pass
