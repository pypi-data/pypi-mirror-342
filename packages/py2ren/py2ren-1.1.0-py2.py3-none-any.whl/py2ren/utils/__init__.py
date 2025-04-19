from . import filepath, iter

def self(it): return it

def toposort(data):
    """
    Taken from toposort package. https://pypi.org/project/toposort/.
    Dependencies are expressed as a dictionary whose keys are items
    and whose values are a set of dependent items. Output is a list of
    sets in topological order. The first set consists of items with no
    dependences, each subsequent set consists of items that depend upon
    items in the preceeding sets.
    """

    # Special case empty input.
    if len(data) == 0:
        return

    # Copy the input so as to leave it unmodified.
    # Discard self-dependencies and copy two levels deep.
    data = {item: set(e for e in dep if e != item) for item, dep in data.items()}

    # Find all items that don't depend on anything.
    extra_items_in_deps = {value for values in data.values() for value in values} - set(
        data.keys()
    )
    # The line below does N unions of value sets, which is much slower than the
    # set comprehension above which does 1 union of N value sets. The speedup
    # gain is around 200x on a graph with 190k nodes.
    # extra_items_in_deps = _reduce(set.union, data.values()) - set(data.keys())

    # Add empty dependences where needed.
    data.update({item: set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if len(dep) == 0)
        if not ordered:
            break
        yield ordered
        data = {
            item: (dep - ordered) for item, dep in data.items() if item not in ordered
        }
    if len(data) != 0:
        raise ValueError("There is likely to be a circular dependence")

def rowchars(text, char, start=0):
    count = 0
    for ch in text[start:]:
        if ch == char:
            count += 1
        elif count != 0:
            break
    return -1 if count == 0 else count


def strip_indexes(source, indexes):
    removed = 0
    for index in indexes:
        del source[index - removed]
        removed += 1

def trymap(func, value, default=None, allow=None):
    if allow is None:
        allow = Exception

    try:
        return func(value)
    except allow:
        return default
