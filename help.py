command_descriptions = {
    "go": """You can move around by typing go, then a direction. Supported directions are north, south, east, west, inside, and outside. You can also just type a direction without saying go, and the go will be implied. Further, you can shorten directions to one letter or short word: n, s, e, w, in, and out.""",
    "look": """If you type look or l by itself, you will get a description of the surrounding area. If you combine it with something visible in the environment, you will get a description of that entity. You can also use examine or x interchangeably with look.""",
    "inventory": """Type inventory or i to see what you're carrying.""",
    "take": """You can pick things up by entering take, then the name of the item you'd like to pick up. Assuming it's not too big.""",
    "eat": """If an entity is edible, you can eat it by typing eat, followed by the name of the edible object.""",
    "exits": "Type exits to see a list of directions you're allowed to move from your current location."
    "",
    "quit": "Quit the garden and return to the command line by typing quit or q.",
    "help": """View these commands.""",
}


def output_commands():
    """Format and output the possible commands in the game."""

    print("*Available commands*:")

    for command in command_descriptions:
        description = command_descriptions[command]
        print()
        print("Command:", command)
        print()
        print(description)


def about():
    """Print some information about the game."""

    print(
        """*About*

This game was created as an instructional aid by Patrick Smyth in October, 2022. The repository for the game is originally at https://github.com/smythp/the_garden."""
    )
