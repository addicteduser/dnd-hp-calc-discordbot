class Flags:
    """A collection of HP modifier flags

    """

    def __init__(self, no_error, is_hilldwarf, axe_attuned, is_tough):
        self.no_error = no_error
        self.is_hilldwarf = is_hilldwarf
        self.axe_attuned = axe_attuned
        self.is_tough = is_tough


class Class:
    """Represents a D&D class.

    Args:
        name (str): The name of the class.
        aliases (list(str)): The list of aliases of the class.
        hit_die (int): The maximum hit die value.

    Attributes:
        name: The name of the class.
        aliases: The list of aliases of the class.
        hit_die: The maximum hit die value.

    """

    def __init__(self, name, aliases, hit_die):
        self.name = name
        self.aliases = aliases
        self.hit_die = hit_die

    def get_class(self, alias):
        """Returns the D&D class given an alias.

        Args:
            alias (str): An alias of the class.

        Returns:
            Class: A D&D class.

        """
        if alias in self.aliases:
            return self
