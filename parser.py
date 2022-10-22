tokens = {
    "directions": [
        "north",
        "south",
        "east",
        "west",
        "northwest",
        "northeast",
        "southeast",
        "southwest",
        "up",
        "down",
        "outside",
        "inside",
        "exit",
        "n",
        "s",
        "e",
        "w",
        "u",
        "d",
        "nw",
        "ne",
        "se",
        "nw",
    ],
    "stopwords": [
        "the",
        "to",
        "on",
        "and",
        "of",
        "at",
        "a",
        "an",
    ],
}


synonyms = {
    "l": "look",
    "scrutinize": "look",
    "examine": "look",
    "x": "look",
    "z": "wait",
    "i": "inventory",
    "out": "outside",
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "u": "up",
    "d": "down",
    "walk": "go",
    "move": "go",
    "run": "go",
    "stroll": "go",
    "amble": "go",
    "q": "quit",
}


def parse(input):

    # Remove all characters except letters and spaces
    only_alphabetical = "".join(
        [letter for letter in input if letter.isalpha() or letter == " "]
    )

    # Remove beginning and ending whitespace and make all characters lower case
    words = only_alphabetical.lower().strip().split()

    # Replace words with synonyms
    replacements = []

    for word in words:
        if word in synonyms:
            replacements.append(synonyms[word])
        else:
            replacements.append(word)

    # Remove stop words
    words = [word for word in replacements if word not in tokens["stopwords"]]

    parsed = {}

    if words[0] in tokens["directions"]:
        parsed["verb"] = "go"
        parsed["direct_object"] = words[0]
    elif words[0] == "in":
        parsed["verb"] = "go"
        parsed["direct_object"] = "inside"
    elif "in" in words:
        in_location = words.index("in")
        parsed["verb"] = words[0]
        parsed["direct_object"] = " ".join(words[1:in_location])
        parsed["indirect_object"] = " ".join(words[in_location + 1 :])
    else:
        parsed["verb"] = words[0]
        parsed["direct_object"] = " ".join(words[1:])

    return parsed
