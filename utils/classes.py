"""Classes

This module provides the classes used in the app."""

# pylint: disable=R0903

from typing import List, Union

from typing_extensions import Self


class Flags:
    """A collection of HP modifier flags."""

    def __init__(
        self, no_error: bool, is_hilldwarf: bool, axe_attuned: bool, is_tough: bool
    ):
        self.no_error = no_error
        self.is_hilldwarf = is_hilldwarf
        self.axe_attuned = axe_attuned
        self.is_tough = is_tough


class DndClass:
    """Represents a D&D class.

    Attributes
    ----------
    name : str
        The name of the class.
    aliases : List[str]
        The list of aliases of the class.
    hit_die : int
        The maximum hit die value.
    """

    def __init__(self, name: str, aliases: List[str], hit_die: int):
        self.name = name
        self.aliases = aliases
        self.hit_die = hit_die

    def get_class(self, alias: str) -> Union[Self, None]:
        """Returns the D&D class given an alias.

        Parameters
        ----------
        alias : str
            An alias of the class.

        Returns
        -------
        Union[Self, None]
            If found, returns the DndClass. Else returns None.
        """
        if alias in self.aliases:
            return self

        return None
