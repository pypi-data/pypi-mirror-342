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
        """Return a new 'Bynd' object instance."""
        data = data
        return super(Bynd, cls).__new__(cls)

    def __init__(self: 'Bynd', data: Any, /) -> None:
        """Initialize a new Bynd object instance."""
        self._data = data
        self._types = set()

    def __dir__(self: 'Bynd', /) -> list[str]:
        """Returns a list of strings corresponding to each 'Bynd' method."""
        attrs = ['__new__', '__init__', '__dir__', '__str__', '__getitem__', 'inner', 'data', 'types']
        return sorted(attrs)

    def __str__(self: 'Bynd', /) -> str:
        """Return a string version of the instantiated Bynd object and its parameters."""
        if self._types is not None and len(self._types) == 1:
            return f"Bynd({self._data!r})[{list(self._types)[0]}]"
        else:
            return f"Bynd({self._data!r})[{self._types}]"

    def __getitem__(self: 'Bynd', /, *types) -> 'Bynd':
        """Repurposed for allowing type specification as a way of binding data to one or more types.
        
        Returns the original Bynd instance with the 'data' and 'types' attributes.
        """
        formattedtypes = ', '.join([_type.__name__ for _type in types])

        if len(types) == 0:
            raise ByndError(f"Bynd(...)[{types!r}] parameter cannot be empty")
        elif not all([ isinstance(_type, (type, type(None))) for _type in types ]):
            raise ByndError(f"Bynd(...)[{formattedtypes!r}] parameters must be of type 'type' or 'None'")
        elif type(self._data) not in types:
            raise ByndError(f"Bynd({self._data!r}) parameter must be of type(s) {formattedtypes}")
        else:
            [self._types.add(T) for T in types]
            return self

    @property
    def types(self: 'Bynd', /) -> set[type]:
        """Get descriptor for the 'types' attribute."""
        return self._types

    @types.setter
    def types(self: 'Bynd', value: Any, /) -> None:
        """Set descriptor for the 'types' attribute."""
        raise ByndError(f"cannot set {value!r} for ReadOnly attribute Bynd.types")

    @types.deleter
    def types(self: 'Bynd', /) -> None:
        """Delete descriptor for the 'types' attribute."""
        raise ByndError(f"cannot delete ReadOnly attribute Bynd.types")

    @property
    def data(self: 'Bynd', /) -> Any:
        """Get descriptor for the 'data' attribute."""
        return self._data

    @data.setter
    def data(self: 'Bynd', value: Any, /) -> None:
        """Set descriptor for the 'data' attribute."""
        raise ByndError(f"cannot set {value!r} for ReadOnly attribute Bynd.data")

    @data.deleter
    def data(self: 'Bynd', /) -> None:
        """Delete descriptor for the 'data' attribute."""
        raise ByndError(f"cannot delete ReadOnly attribute Bynd.data")

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

    def __traverse_mapping__(self: 'Bynd', outerdata: Any, /, *types) -> None:
        """Traverses and validates the inner types for a collection mapping."""
        formattedtypes = [_type.__name__ for _type in types]
        innerdata_temp = [outerdata]

        while len(innerdata_temp) != 0:
            innerdata = innerdata_temp.pop()

            for innerdata_key, innerdatadata in innerdata.items():
                if type(innerdatadata) not in types:
                    raise ByndError(f"Bynd(data{outerdata}).inner({innerdatadata}) must be of type(s) {formattedtypes}")
                elif self.__retrieve__(innerdata_key) == "sequence":
                    self.__traverse_sequence__(list(innerdata_key), *types)
                elif self.__retrieve__(innerdatadata) == "mapping":
                    innerdata_temp.insert(0, innerdatadata)
                else:
                    continue

    def __traverse_sequence__(self: 'Bynd', outerdata: Any, /, *types) -> None:
        """Traverses and validates the inner types for a collection sequence."""
        formattedtypes = [_type.__name__ for _type in types]
        innerdata_temp = [outerdata]

        while len(innerdata_temp) != 0:
            innerdata = innerdata_temp.pop()

            for innerdata_item in innerdata:
                if type(innerdata_item) not in types:
                    raise ByndError(f"Bynd(data={outerdata}).inner({innerdata_item}) must be of types(s) {formattedtypes}")
                elif self.__retrieve__(innerdata_item) == "sequence":
                    innerdata_temp.insert(0, innerdata_item)
                elif self.__retrieve__(innerdata_item) == "mapping":
                    self.__traverse_mapping__(innerdata_item, *types)
                else:
                    continue

    def inner(self: 'Bynd', /, *types) -> 'Bynd':
        """Allows type specification for collection inner types such as dict, frozenset, list, set, tuple, and others."""
        [self._types.add(T) for T in types]

        if len(types) == 0:
            raise ByndError(f"Bynd(...).inner(*types=()) parameters cannot be empty")
        elif not all([ isinstance(T, type) for T in types ]):
            raise ByndError(f"Bynd(...).inner(*types={types}) parameter items must be of type 'type'")
        elif self.__retrieve__(self._data) == "mapping":
            self.__traverse_mapping__(dict(self._data), *types)
            return self
        elif self.__retrieve__(self._data) == "sequence":
            self.__traverse_sequence__(list(self._data), *types)
            return self
        else:
            return self
