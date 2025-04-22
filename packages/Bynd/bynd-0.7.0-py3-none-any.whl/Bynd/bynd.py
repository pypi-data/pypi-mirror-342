"""A module which allows binding values to one or more types.

The most common use case would be to use bynd as if were an

alias. When assigning a bynd object to a variable, the user

will get runtime type checking, a bynd object in return, and

access to the supplied value as well as the supplied types, 

where the value can be used the same way a variable would be 

used. The only inconvienence would be having to use the dot 

operator when accessing the value from the bynd object and 

maybe having to declare, define and instantiate a bynd object 

each time.
"""


import sys
from collections import defaultdict, deque, UserDict, UserList, OrderedDict
from typing import Any


class byndError(BaseException):
    """Custom error for the 'bynd' class."""
    __slots__ = frozenset({})

    def __new__(cls: type['byndError'], message: str, /) -> 'byndError':
        """Return a new 'byndError' object."""
        assert isinstance(message, str), f"'{message}' must be of type 'str'"
        return super(byndError, cls).__new__(cls)

    def __init__(self: 'byndError', message: str | None) -> None:
        """Initialize a 'byndError' object instance."""
        super().__init__(message)
        self.__suppress_context__ = True
        sys.tracebacklimit = 0


class bynd(object):
    """Binds the specified value to one or more types.

    my_variable = bynd('some string')[str]
    print(my_variable.value)

    In the example above, 'some string' is bound to the type

    str. When 'some string' is changed to any other type a 

    byndError will be raised.
    """
    __slots__ = frozenset({'types', 'value'})

    def __new__(cls: type['bynd'], value: Any, /) -> 'bynd':
        """Return a new 'bynd' object."""
        value = value
        return super(bynd, cls).__new__(cls)

    def __init__(self: 'bynd', value: Any, /) -> None:
        """Initialize a new bynd object instance."""
        self.value = value
        self.types = None

    def __str__(self: 'bynd', /) -> str:
        """Return a string version of the instantiated bynd object and its parameters."""
        if self.types is not None and len(self.types) == 1:
            return f"bynd({self.value!r} = {self.types[0]})"
        else:
            return f"bynd({self.value!r} = {self.types})"

    def __getitem__(self: 'bynd', /, *types) -> 'bynd':
        """Repurposed for allowing type specification as a way of binding a value to one or more types.
        
        Returns the original bynd instance with the value and types attributes.
        """
        if len(types) == 0:
            raise byndError(f"bynd(...)[{types!r}] parameter cannot be empty")
        elif not all([ isinstance(_type, (type, type(None))) for _type in types ]):
            formatted_types = ', '.join([_type for _type in types])
            raise byndError(f"bynd(...)[{formatted_types!r}] parameters must be of type 'type' or 'None'")
        elif type(self.value) not in types:
            print(type(self.value), types)
            formatted_types = tuple([_type.__name__ for _type in types])
            raise byndError(f"bynd({self.value!r}) parameter must be of type(s) {formatted_types}")
        else:
            self.types = types
            return self

    def inner_types(self: 'bynd', keys: list[type] = [], values: list[type] = [], others: list[type] = []) -> None:
        """Allows inner type specification for collection types such as lists, tuples, dicts, sets, as well as others."""
        formatted_keys = [_type.__name__ for _type in keys] if len(keys) > 0 else "[]"
        formatted_values = [_type.__name__ for _type in values] if len(values) > 0 else "[]"
        formatted_others = [_type.__name__ for _type in others] if len(others) > 0 else "[]"

        match self.value:
            case defaultdict() | dict() | OrderedDict() | UserDict():
                if len(others) > 0:
                    raise byndError(f"bynd.inner_types({others}) parameter must be empty")
                elif (len(keys) > 0) and (len(values) > 0):
                    for key,value in self.value.items():
                        if type(key) not in keys:
                            raise byndError(f"bynd(value={self.value}) inner_key {key} must be of type(s) {formatted_keys}")
                        elif type(value) not in values:
                            raise byndError(f"bynd(value={self.value}) inner_value {value} must be of type(s) {formatted_values}")
                        elif type(value) in [defaultdict, dict, OrderedDict, UserDict]:
                            if not all([type(item) in keys for item in value.keys()]):
                                raise byndError(f"bynd(value={self.value}) {value} inner_keys must be of type(s) {formatted_keys}")
                            elif not all([type(item) in values for item in value.values()]):
                                raise byndError(f"bynd(value={self.value}) {value} inner_values must be of type(s) {formatted_values}")
                            else:
                                continue
                        else:
                            continue
                else:
                    raise byndError(f"bynd.inner_types(keys={keys}, values={values}) parameters cannot be empty")

            case deque() | list() | frozenset() | set() | tuple() | UserList():
                if (len(keys) > 0) and (len(values) > 0):
                    raise byndError(f"bynd.inner_types(others={others}) parameter must be empty")
                elif len(others) > 0:
                    for value in self.value:
                        if type(value) not in others:
                            raise byndError(f"bynd(value={self.value}) inner_item {value} must be of type(s) {formatted_others}")
                        elif type(value) in [list, frozenset, set, tuple, UserList]:
                            if not all([type(item) in others for item in value]):
                                raise byndError(f"bynd({self.value}) {value} inner_items must be of types(s) {formatted_others}")
                            else:
                                continue
                        else:
                            continue
                else:
                    raise byndError(f"bynd.inner_types(others={others}) parameter cannot be empty")

            case _:
                raise byndError(f"bynd(value={self.value}) parameter must be a collection type")
