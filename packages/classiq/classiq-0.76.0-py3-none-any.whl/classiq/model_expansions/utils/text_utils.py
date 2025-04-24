def s(items: list) -> str:
    return "" if len(items) == 1 else "s"


def are(items: list) -> str:
    return "is" if len(items) == 1 else "are"


def they(items: list) -> str:
    return "it" if len(items) == 1 else "they"


def readable_list(items: list) -> str:
    if len(items) == 1:
        return str(items[0])
    return f"{', '.join(items[:-1])} and {items[-1]}"
