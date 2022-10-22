from parser import parse
from utilities import prose_iterator, first_case, clear, simplify_name


debug = False
run_game = True


class Location:
    """A class representing locations."""

    # A list to keep track of all locations
    all = []

    def __init__(
        self,
        name,
        description="A place",
        north=False,
        south=False,
        east=False,
        west=False,
        inside=False,
        outside=False,
        contents=False,
    ):
        """Instantiate a location object."""
        self.name = name
        self.description = description
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.inside = inside
        self.outside = outside
        self.contents = contents or []

        for entity in self.contents:
            entity.location = self

        if self.north:
            self.north.south = self
        if self.south:
            self.south.north = self
        if self.inside:
            self.inside.outside = self
        if self.outside:
            self.outside.inside = self
        if self.east:
            self.east.west = self
        if self.west:
            self.west.east = self

        Location.all.append(self)

    def simplified_name(self):
        """Return the location's name in lower case and with no articles."""
        return simplify_name(self.name)

    def all_present(self, entity=False):
        """Generate a list of all entities present at the location."""

        out = []

        if entity:
            contents = entity.contents
        else:
            contents = self.contents

        for o in contents:
            out.append(o)
            if o.contents:
                out += self.all_present(entity=o)

        return out

    def is_present(self, thing_or_string):
        """Check if an object is present, either in the location or in a container in the location, including the player."""

        entities_list = self.all_present()

        if isinstance(thing_or_string, str):
            for entity in entities_list:
                if entity.match_name(thing_or_string):
                    return entity
        else:
            for entity in entities_list:
                if thing_or_string is entity:
                    return entity

        return False

    def directions(self):
        return {
            "north": self.north,
            "south": self.south,
            "east": self.east,
            "west": self.west,
            "inside": self.inside,
            "outside": self.outside,
        }

    def exits(self):
        return {
            direction: self.directions()[direction]
            for direction in self.directions()
            if self.directions()[direction]
        }

    def add(self, thing):
        """Add something to the location."""
        if thing.location and thing in thing.location.contents:
            thing.location.contents.remove(thing)
        self.contents.append(thing)
        thing.location = self

    def __repr__(self):
        return f"<Location: {self.name}>"

    def __str__(self):
        return self.name


class Entity:
    """An object representing a living or nonliving thing."""

    def __init__(
        self,
        name,
        location=False,
        description="Something quite mysterious",
        edible=False,
        eat_description=False,
        big=False,
        player=False,
        contents=False,
        proper=False,
        aliases=False,
    ):
        """Instantiate an entity."""
        self.name = name
        self.description = description
        self.location = location
        self.edible = edible
        self.proper = proper
        self.eat_description = eat_description
        self.big = big
        self.aliases = (aliases or [],)
        self.player = player

        self.contents = contents or []

        for entity in self.contents:
            entity.location = self

        if self.location:
            self.location.add(self)

    def __repr__(self):
        return f"<Entity: {self.name}>"

    def lower_case_name(self):
        """Give the entitty's name in lower case if the entity isn't a proper noun."""

        if self.proper:
            return self.name
        else:
            return self.name.lower()

    def __str__(self):
        return self.name

    def change_location(self, new_location):
        """Change the location of this object."""
        new_location.add(self)
        self.location = new_location

    def destroy(self):
        self.location.contents.remove(self)
        del self

    def add(self, thing):
        """Put something in this entity."""
        if thing.location and thing in thing.location.contents:
            thing.location.contents.remove(thing)
        self.contents.append(thing)
        thing.location = self

    def inventory(self):
        """Print the contents of the entity."""
        stuff = prose_iterator(self.contents)

        if self.player:
            if stuff:
                print(f"{self.name} is carrying {stuff}.")
            else:
                print(f"{self.name} isn't carrying anything.")
        else:
            if stuff:
                print(f"{self.article_name} contains {stuff}")
            else:
                print(f"{self.article_name} doesn't have anyting in it.")

    def look(self):
        """Print a description of the current location and visible entities."""
        print(self.location.name)
        print()
        print(self.location.description)

        if self.location.contents:
            print()
            print(f"You see here {prose_iterator(self.location.contents)}")

    def simplified_name(self):
        """Return the entity's name in lower case and with no articles."""
        return simplify_name(self.name)

    def match_name(self, name):
        """Given a string, return true if the string is the entity's simplified name or an alias."""

        return (
            name == self.simplified_name() or name == self.name or name in self.aliases
        )

    def article(self):
        """Generate an appropriate article for this entity based on whether it is proper and the first letter."""

        if not self.name:
            return ""

        lower = self.name.lower()
        if self.proper and not lower.startswith("the"):
            return "the"
        elif self.proper:
            return ""

        if (
            self.name[0]
            in (
                "a",
                "e",
                "i",
                "o",
                "u",
            )
            and not self.name.lower().startswith("an ")
        ):
            return "an"
        elif self.name[0] in ("a", "e", "i", "o", "u") and self.name.lower().startswith(
            "an "
        ):
            return ""

        if not self.proper and not self.name.lower().startswith("a "):
            return "a"
        else:
            return ""

    def article_name(self, upper=False):
        """Return name with article attached."""

        if self.article():
            seperator = " "
        else:
            seperator = ""

        out = self.article() + seperator + self.lower_case_name()
        if upper:
            out = first_case(out, case="upper")

        return out

    def take(self, thing):
        """Take something if it's not big."""
        if not thing.big:
            print(f"You take the {thing.lower_case_name()}")
            self.add(thing)
            return True
        else:
            print(f"The {thing.lower_case_name()} is too big to take.")
            return False

    def examine(self, thing):
        """Take a look at something."""

        print(
            f"""You examine {thing.article_name()}.

{thing.description}"""
        )

    def drop(self, thing):
        """Drop an item at current location."""
        if thing in self.contents:
            print(f"You drop the {thing.lower_case_name()}.")
            self.location.add(thing)
            return True
        else:
            print("You're not carrying that.")
            return False

    def move(self, direction):
        """Move in a specific direction."""

        direction = direction.lower()

        if direction not in self.location.exits():
            print(f"You cannot move {direction} from here.")
            return False
        else:
            new_location = self.location.exits()[direction]
            self.change_location(new_location)
            print(f"You move toward the {new_location.simplified_name()}.")
            return True

    def eat(self, foodstuff):
        if not foodstuff.edible:
            print("That's not edible.")
            return False
        if foodstuff.eat_description:
            print(foodstuff.eat_description)
        else:
            print(f"You chow down on the {foodstuff.name}. Pretty tasty.")

        foodstuff.destroy()
        return True


cottage = Location(
    "A little cottage",
    description="A small thatch-roofed structure, surrounded by verdant green",
)

inside_cottage = Location(
    "Cozy interior of a little cottage",
    description="The functional yet comfortable interior to the small cottage in the center of the garden. A large pot hangs in the fireplace.",
    outside=cottage,
    contents=[
        Entity(
            "A pot",
            description="A large cast-iron pot, ideal for simmering stews and brewing potations.",
            big=True,
        )
    ],
)


pumpkin_patch = Location(
    "Pumpkin patch",
    description="A pumpkin patch. Curly vines wrap around ripe orange pumpkins.",
    east=cottage,
)

realy_big_pumpkin = Entity(
    "Really big pumpkin",
    description="This enormous pumpkin is truly formidable.",
    location=pumpkin_patch,
    edible=True,
    big=True,
)

normal_pumpkin = Entity(
    "Fairly normal pumpkin",
    description="This pumpkin is about the size you'd expect from a vegetable of family cucurbitaceae.",
    location=pumpkin_patch,
    edible=True,
)
weird_shaped_pumpkin = Entity(
    "Weirdly shaped pumpkin",
    description="There's always one. This pumpkin is shaped like a starfish and it's orange color is streaked with green",
    location=pumpkin_patch,
    edible=True,
)


player = Entity(
    "The Gardener",
    description="A creature of sun and soil. You tend the land.",
    player=True,
    location=cottage,
    proper=True,
    contents=[
        Entity("Trowel", description="A simple hand tool for turning over the soil.")
    ],
)

print(
    """"

The Garden

An example game created to show simple parsing and use of an object-oriented approach to game creation.

* * *

You stand in front of your small cottage, surrounded by verdant life. You are the gardener.

Press return to continue.
"""
)

input()
clear()
player.look()


# Game loop
while run_game:
    commands = parse(input(" > "))

    if debug:
        print(commands)

    verb, direct, indirect = (
        commands.get("verb"),
        commands.get("direct_object"),
        commands.get("indirect_object"),
    )

    # Map the direct object name to a game entity
    present_direct = player.location.is_present(direct)

    if verb == "go":
        player.move(direct)

    if verb == "look":
        if not present_direct:
            player.look()
        else:
            if present_direct:
                player.examine(present_direct)
            else:
                print(f"You dont' see a {direct} here to scrutinize.")

    if verb == "quit":
        print("Departing the garden...")
        run_game = False
    if verb == "clear":
        clear()
    if verb == "inventory":
        player.inventory()
    if verb == "exits":
        exits = prose_iterator(player.location.exits().keys())

        print(f"From here you can move {exits}.")
    if verb == "take":
        if present_direct:
            player.take(present_direct)
        else:
            print(f"You don't see a {direct} here to take.")

    if verb == "eat":
        if present_direct:
            player.eat(present_direct)
        else:
            print(f"You don't see a {direct} here to chow down on.")

    if verb == "wait":
        print("Time passes...")

    if verb == "drop" and not present_direct:
        print(f"You don't have a {direct} to drop.")
    elif verb == "drop" and present_direct:
        player.drop(present_direct)
