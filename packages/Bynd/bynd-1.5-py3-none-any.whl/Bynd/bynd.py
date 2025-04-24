"""A module which allows binding data to one or more types.

Bynd's intended use, is to be assigned to a variable.

Which, in this case, the variable can still be used

exactly the same way just by accessing the 'data'

class attribute. Since 'Bynd' "binds" the data to 

one or more types, the data cannot be modified

causing it to be constant and forces the programmer

to create references which can be modified.
   
The benefits of using Bynd are:

1. Runtime type checking

2. Constant data
   
3. Ability to access the bound data
   and its types with the '__info__'
   class attribute or just the data
   itself from the variable in which
   it is stored using the '.' operator
"""


import sys
from typing import Any
from collections import defaultdict, deque, UserDict, UserList, OrderedDict


def __dir__() -> list[str]:
    """Returns a list of strings corresponding to each 'Bynd' module object."""
    attrs = ['ByndError', 'Bynd']
    return sorted(attrs)


class ByndError(BaseException):
    """Custom error for the 'Bynd' class."""
    __slots__ = frozenset({})

    def __new__(cls: type['ByndError'], message: str, /) -> 'ByndError':
        """Return a new 'ByndError' object."""
        assert isinstance(message, str), f"'{message}' must be of type 'str'"
        return super(ByndError, cls).__new__(cls)

    def __init__(self: 'ByndError', message: str | None) -> None:
        """Initialize a 'ByndError' object instance."""
        super().__init__(message)
        self.__suppress_context__ = True
        sys.tracebacklimit = 0

    def __dir__(self: 'ByndError', /) -> list[str]:
        """Returns a list of strings corresponding to each 'ByndError' method."""
        attrs = ['__new__', '__init__']
        return sorted(attrs)


class Bynd(object):
    """Binds data to one or more types.

    Usage:
        bound_data = Bynd("some string", {str})
        print(bound_data.data)

    In the example above, '"some string"'

    is bound to the type 'str'. Otherwise, 

    a ByndError is raised.
    """
    __slots__ = frozenset({})

    def __new__(cls: type['Bynd'], data: Any, types: set[type], /) -> 'Bynd':
        """Return a new 'Bynd' object instance."""
        cls.__info__ = {data: types}
        cls.data = cls.__validate__(data, types)
        return super(Bynd, cls).__new__(cls)

    def __dir__(self: 'Bynd', /) -> list[str]:
        """Returns a list of strings corresponding to each 'Bynd' method."""
        attrs = ['__new__', '__init__', '__dir__', '__info__']
        return sorted(attrs)

    def __hash__(self: 'Bynd', /) -> int:
        """Allow 'Bynd' to be hashable."""
        return hash(self)

    @classmethod
    def __retrieve__(cls: type['Bynd'], data: Any, /) -> str:
        """Get the current type of the data to be bound."""
        if isinstance(data, (defaultdict, dict, OrderedDict, UserDict)):
            return "mapping"
        if isinstance(data, (deque, list, frozenset, set, tuple, UserList)):
            return "sequence"
        else:
            return "regular"

    @classmethod
    def __main_check__(cls: type['Bynd'], data: Any, types: set[type], /) -> Any:
        """Perform checks on types that are not collection types."""
        formatted_types = '{' + ', '.join([_type.__name__ for _type in types]) + '}'

        if len(types) == 0:
            raise ByndError(f"Bynd(...)[{formatted_types!r}] parameter cannot be empty")
        elif not all([ isinstance(_type, (type, type(None))) for _type in types ]):
            raise ByndError(f"Bynd(...)[{formatted_types!r}] parameters must be of type 'type' or 'None'")
        elif type(data) not in types:
            raise ByndError(f"Bynd({data!r}) parameter must be of type(s) {formatted_types}")
        else:
            return data

    @classmethod
    def __traverse_mapping__(cls: type['Bynd'], data: Any, types: set[type], /) -> object:
        """Traverses and validates the inner types for a collection mapping."""
        formatted_types = '{' + ', '.join([_type.__name__ for _type in types]) + '}'
        inner_data_temp = [data]

        while len(inner_data_temp) != 0:
            inner_data = inner_data_temp.pop()

            for inner_data_key, inner_data_data in inner_data.items():
                if type(inner_data_data) not in types:
                    raise ByndError(f"Bynd({data}) item({inner_data_data}): must be of type(s) {formatted_types}")
                elif cls.__retrieve__(inner_data_key) == "sequence":
                    cls.__traverse_sequence__(list(inner_data_key), types)
                elif cls.__retrieve__(inner_data_data) == "mapping":
                    inner_data_temp.insert(0, inner_data_data)
                else:
                    continue
        else:
            return data

    @classmethod
    def __traverse_sequence__(cls: type['Bynd'], data: Any, types: set[type], /) -> Any:
        """Traverses and validates the inner types for a collection sequence."""
        formatted_types = '{' + ', '.join([_type.__name__ for _type in types]) + '}'
        inner_data_temp = [data]

        while len(inner_data_temp) != 0:
            inner_data = inner_data_temp.pop()

            for inner_data_item in inner_data:
                if type(inner_data_item) not in types:
                    raise ByndError(f"Bynd({data}) item({inner_data_item}): must be of types(s) {formatted_types}")
                elif cls.__retrieve__(inner_data_item) == "sequence":
                    inner_data_temp.insert(0, inner_data_item)
                elif cls.__retrieve__(inner_data_item) == "mapping":
                    cls.__traverse_mapping__(inner_data_item, types)
                else:
                    continue
        else:
            return data

    @classmethod
    def __validate__(cls: type['Bynd'], data: Any, types: set[type], /) -> Any:
        """Allows type specification for collection inner types such as dict, frozenset, list, set, tuple, and others."""
        formatted_types = '{' + ', '.join([_type.__name__ for _type in types]) + '}'

        if len(types) == 0:
            raise ByndError("Bynd(..., {}) parameters cannot be empty")
        elif not all([ isinstance(T, type) for T in types ]):
            raise ByndError(f"Bynd(..., {formatted_types}) parameters must be of type 'type'")
        elif cls.__retrieve__(data) == "mapping":
            data = cls.__main_check__(data, types)
            return cls.__traverse_mapping__(dict(data), types)
        elif cls.__retrieve__(data) == "sequence":
            data = cls.__main_check__(data, types)
            return cls.__traverse_sequence__(list(data), types)
        else:
            return cls.__main_check__(data, types)
