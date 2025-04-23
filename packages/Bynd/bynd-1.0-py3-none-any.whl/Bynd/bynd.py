"""A module which allows binding datas to one or more types.

Bynd's intended use case is to be assigned to a variable.
   
The benefits of using Bynd are static type checking at runtime
   
and being able to access the bound data and types. A variable,
   
in this case, can still be used the same way with one simple

change; using the dot operator to access the data.
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

    my_variable = Bynd("some string")[str]
    print(my_variable.data)

    In the example above, '"some string"' is bound to the type

    str. When '"some string"' is changed to any other type, a 

    ByndError will be raised.
    """
    __slots__ = frozenset({'_types', '_data'})

    def __new__(cls: type['Bynd'], data: Any, /) -> 'Bynd':
        """Return a new 'Bynd' object."""
        data = data
        return super(Bynd, cls).__new__(cls)

    def __init__(self: 'Bynd', data: Any, /) -> None:
        """Initialize a new Bynd object instance."""
        self._data = data
        self._types = set()

    @property
    def types(self: 'Bynd', /) -> Any:
        """The 'types' instance variable property."""
        return self._types

    @property
    def data(self: 'Bynd', /) -> Any:
        """The 'data' instance variable property."""
        return self._data

    @types.setter
    def types(self: 'Bynd', data: Any, /) -> Any:
        """The 'types' instance variable property."""
        formatted_types = ', '.join([_type.__name__ for _type in self._types])
        raise ByndError(f"Bynd(...)[{formatted_types}] cannot modify bound types with '{data}'")

    @data.setter
    def data(self: 'Bynd', data: Any, /) -> None:
        """The 'data' instance variable setter property."""
        raise ByndError(f"Bynd(data={self._data}) cannot modify bound data with '{data}'")

    def __dir__(self: 'Bynd', /) -> list[str]:
        """Returns a list of strings corresponding to each 'Bynd' method."""
        attrs = ['__new__', '__init__', '__dir__', '__str__', '__getitem__', 'inner', 'data', 'types']
        return sorted(attrs)

    def __str__(self: 'Bynd', /) -> str:
        """Return a string version of the instantiated Bynd object and its parameters."""
        if self.types is not None and len(self.types) == 1:
            return f"Bynd({self.data!r} = {list(self.types)[0]})"
        else:
            return f"Bynd({self.data!r} = {self.types})"

    def __getitem__(self: 'Bynd', /, *types) -> 'Bynd':
        """Repurposed for allowing type specification as a way of binding a data to one or more types.
        
        Returns the original Bynd instance with the data and types attributes.
        """
        formatted_types = ', '.join([_type.__name__ for _type in types])

        if len(types) == 0:
            raise ByndError(f"Bynd(...)[{types!r}] parameter cannot be empty")
        elif not all([ isinstance(_type, (type, type(None))) for _type in types ]):
            raise ByndError(f"Bynd(...)[{formatted_types!r}] parameters must be of type 'type' or 'None'")
        elif type(self.data) not in types:
            raise ByndError(f"Bynd({self.data!r}) parameter must be of type(s) {formatted_types}")
        else:
            [self._types.add(T) for T in types]
            return self

    def __retrieve__(self: 'Bynd', data: Any, /) -> str | None:
        """Get the current type of the data to be bound."""
        data_type = None
        if isinstance(data, (defaultdict, dict, OrderedDict, UserDict)):
            data_type = "mapping"
            return data_type
        if isinstance(data, (deque, list, frozenset, set, tuple, UserList)):
            data_type = "sequence"
            return data_type
        else:
            return data_type

    def __traverse_mapping__(self: 'Bynd', outer_data: Any, /, *types) -> None:
        """Traverses and validates the inner types for a collection mapping."""
        formatted_types = [_type.__name__ for _type in types]
        inner_data_temp = [outer_data]

        while len(inner_data_temp) != 0:
            inner_data = inner_data_temp.pop()

            for inner_data_key, inner_data_data in inner_data.items():
                if type(inner_data_data) not in types:
                    raise ByndError(f"Bynd(data{outer_data}).inner({inner_data_data}) must be of type(s) {formatted_types}")
                elif self.__retrieve__(inner_data_key) == "sequence":
                    self.__traverse_sequence__(list(inner_data_key), *types)
                elif self.__retrieve__(inner_data_data) == "mapping":
                    inner_data_temp.insert(0, inner_data_data)
                else:
                    continue

    def __traverse_sequence__(self: 'Bynd', outer_data: Any, /, *types) -> None:
        """Traverses and validates the inner types for a collection sequence."""
        formatted_types = [_type.__name__ for _type in types]
        inner_data_temp = [outer_data]

        while len(inner_data_temp) != 0:
            inner_data = inner_data_temp.pop()

            for inner_data_item in inner_data:
                if type(inner_data_item) not in types:
                    raise ByndError(f"Bynd(data={outer_data}).inner({inner_data_item}) must be of types(s) {formatted_types}")
                elif self.__retrieve__(inner_data_item) == "sequence":
                    inner_data_temp.insert(0, inner_data_item)
                elif self.__retrieve__(inner_data_item) == "mapping":
                    self.__traverse_mapping__(inner_data_item, *types)
                else:
                    continue

    def inner(self: 'Bynd', /, *types) -> None:
        """Allows type specification for collection inner types such as dict, frozenset, list, set, tuple, and others."""
        [self._types.add(T) for T in types]

        if len(types) == 0:
            raise ByndError(f"Bynd(...).inner(*types=()) parameters cannot be empty")
        elif not all([ isinstance(T, type) for T in types ]):
            raise ByndError(f"Bynd(...).inner(*types={types}) parameter items must be of type 'type'")
        elif self.__retrieve__(self.data) == "mapping":
            self.__traverse_mapping__(dict(self.data), *types)
        elif self.__retrieve__(self.data) == "sequence":
            self.__traverse_sequence__(list(self.data), *types)
        else:
            return None
