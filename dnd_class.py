class Class:
    """Short summary.

    Args:
        name (type): Description of parameter `name`.
        aliases (type): Description of parameter `aliases`.
        hit_die (type): Description of parameter `hit_die`.

    Attributes:
        name
        aliases
        hit_die

    """

    def __init__(self, name, aliases, hit_die):
        self.name = name
        self.aliases = aliases
        self.hit_die = hit_die

    def get_name(self, alias):
        """Returns the name of the class given one of its aliases.

        Args:
            alias (String): An alias of the class.

        Returns:
            String: The name of the class.

        """
        if alias in self.aliases:
            return self.name

    def get_hit_dice(self, name):
        """Returns the hit die value of the class.

        Args:
            name (type): Description of parameter `name`.

        Returns:
            type: Description of returned object.

        """
        if name == self.name:
            return self.hit_die


# class1 = Class('Artificer', ['artificer', 'art', 'a'], 8)
# print(class1.get_name('art'))
# print(class1.get_hit_dice('Artificer'))
