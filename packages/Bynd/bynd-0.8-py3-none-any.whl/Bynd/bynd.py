"""A module which allows binding values to one or more types.

Bynd is intended use case is to be assigned to a variable.
   
The benefits of using Bynd are static type checking at runtime
   
and being able to access the bound value and types. A variable,
   
in this case, can still be used the same way with one simple

change; using the dot operator to access the value.
"""


import sys
from collections import defaultdict, deque, UserDict, UserList, OrderedDict
from typing import Any


def __dir__() -> list[str]:
    """Returns a list of strings corresponding to each 'Bynd' module object."""
    attrs = ['ByndError', 'Bynd', '__dir__']
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
    """Binds the specified value to one or more types.

    my_variable = Bynd('some string')[str]
    print(my_variable.value)

    In the example above, 'some string' is bound to the type

    str. When 'some string' is changed to any other type a 

    ByndError will be raised.
    """
    __slots__ = frozenset({'_types', '_value'})

    def __new__(cls: type['Bynd'], value: Any, /) -> 'Bynd':
        """Return a new 'Bynd' object."""
        value = value
        return super(Bynd, cls).__new__(cls)

    def __init__(self: 'Bynd', value: Any, /) -> None:
        """Initialize a new Bynd object instance."""
        self._value = value
        self._types = set()

    @property
    def types(self: 'Bynd', /) -> Any:
        """The 'types' instance variable property."""
        return self._types

    @property
    def value(self: 'Bynd', /) -> Any:
        """The 'value' instance variable property."""
        return self._value

    @types.setter
    def types(self: 'Bynd', value: Any, /) -> Any:
        """The 'types' instance variable property."""
        formatted_types = ', '.join([_type.__name__ for _type in self._types])
        raise ByndError(f"Bynd(...)[{formatted_types}] cannot modify bound types with '{value}'")

    @value.setter
    def value(self: 'Bynd', value: Any, /) -> None:
        """The 'value' instance variable setter property."""
        raise ByndError(f"Bynd(value={self._value}) cannot modify bound value with '{value}'")

    def __dir__(self: 'Bynd', /) -> list[str]:
        """Returns a list of strings corresponding to each 'Bynd' method."""
        attrs = ['__new__', '__init__', '__dir__', '__str__', '__getitem__', 'inner']
        return sorted(attrs)

    def __str__(self: 'Bynd', /) -> str:
        """Return a string version of the instantiated Bynd object and its parameters."""
        if self.types is not None and len(self.types) == 1:
            return f"Bynd({self.value!r} = {list(self.types)[0]})"
        else:
            return f"Bynd({self.value!r} = {self.types})"

    def __getitem__(self: 'Bynd', /, *types) -> 'Bynd':
        """Repurposed for allowing type specification as a way of binding a value to one or more types.
        
        Returns the original Bynd instance with the value and types attributes.
        """
        formatted_types = ', '.join([_type.__name__ for _type in types])

        if len(types) == 0:
            raise ByndError(f"Bynd(...)[{types!r}] parameter cannot be empty")
        elif not all([ isinstance(_type, (type, type(None))) for _type in types ]):
            raise ByndError(f"Bynd(...)[{formatted_types!r}] parameters must be of type 'type' or 'None'")
        elif type(self.value) not in types:
            raise ByndError(f"Bynd({self.value!r}) parameter must be of type(s) {formatted_types}")
        else:
            [self._types.add(T) for T in types]
            return self

    def __retrieve__(self: 'Bynd', value: Any, /) -> str | None:
        """Get the current type of the value to be bound."""
        value_type = None
        if isinstance(value, (defaultdict, dict, OrderedDict, UserDict)):
            value_type = "mapping"
            return value_type
        if isinstance(value, (deque, list, frozenset, set, tuple, UserList)):
            value_type = "sequence"
            return value_type
        else:
            return value_type

    def __traverse_mapping__(self: 'Bynd', outer_value: Any, /, *types) -> None:
        """Traverses and validates the inner types for a collection mapping."""
        formatted_types = [_type.__name__ for _type in types]
        inner_value_temp = [outer_value]

        while len(inner_value_temp) != 0:
            inner_value = inner_value_temp.pop()

            for inner_value_key, inner_value_value in inner_value.items():
                if type(inner_value_value) not in types:
                    raise ByndError(f"Bynd(value{outer_value}).inner({inner_value_value}) must be of type(s) {formatted_types}")
                elif self.__retrieve__(inner_value_key) == "sequence":
                    self.__traverse_sequence__(list(inner_value_key), *types)
                elif self.__retrieve__(inner_value_value) == "mapping":
                    inner_value_temp.insert(0, inner_value_value)
                else:
                    continue

    def __traverse_sequence__(self: 'Bynd', outer_value: Any, /, *types) -> None:
        """Traverses and validates the inner types for a collection sequence."""
        formatted_types = [_type.__name__ for _type in types]
        inner_value_temp = [outer_value]

        while len(inner_value_temp) != 0:
            inner_value = inner_value_temp.pop()

            for inner_value_item in inner_value:
                if type(inner_value_item) not in types:
                    raise ByndError(f"Bynd(value={outer_value}).inner({inner_value_item}) must be of types(s) {formatted_types}")
                elif self.__retrieve__(inner_value_item) == "sequence":
                    inner_value_temp.insert(0, inner_value_item)
                elif self.__retrieve__(inner_value_item) == "mapping":
                    self.__traverse_mapping__(inner_value_item, *types)
                else:
                    continue

    def inner(self: 'Bynd', /, *types) -> None:
        """Allows type specification for collection inner types such as dict, frozenset, list, set, tuple, and others."""
        [self._types.add(T) for T in types]

        if len(types) == 0:
            raise ByndError(f"Bynd(...).inner(*types=()) parameters cannot be empty")
        elif not all([ isinstance(T, type) for T in types ]):
            raise ByndError(f"Bynd(...).inner(*types={types}) parameter items must be of type 'type'")
        elif self.__retrieve__(self.value) == "mapping":
            self.__traverse_mapping__(dict(self.value), *types)
        elif self.__retrieve__(self.value) == "sequence":
            self.__traverse_sequence__(list(self.value), *types)
        else:
            return None
