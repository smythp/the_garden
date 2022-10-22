from os import system, name


def first_case(s, case="lower"):
    """Change the case of the first character of a string."""

    if not s:
        raise ValueError("String must evaluate to True.")

    case_map = {"lower": s[0].lower, "upper": s[0].upper}

    return case_map[case]() + s[1:]


def prose_iterator(iterator, raw=False):
    """Return a string of prose describing a list of objects. Uses object name attributes by default. If raw, use the string representation"""

    if iterator:
        out = []
        for item in iterator:
            if isinstance(item, str):
                out.append(item)
            else:
                out.append(item.article_name())

    iterator = out

    if len(iterator) > 2:
        prose_output = ", ".join(iterator[:-1])
        prose_output += f", and {iterator[-1]}"
    elif len(iterator) == 2:
        prose_output = " and ".join(iterator)
    elif len(iterator) == 1:

        prose_output = str(iterator[-1])
    else:
        return ""

    return prose_output


def clear():
    """Clears the screen."""
    # for windows
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def simplify_name(name):
    """Create a simplified version of anem, with no articles and lower case."""
    name = name.lower()

    for article in ("the", "an", "a"):
        article += " "
        if name.startswith(article):
            name = name[len(article) :]
    return name
