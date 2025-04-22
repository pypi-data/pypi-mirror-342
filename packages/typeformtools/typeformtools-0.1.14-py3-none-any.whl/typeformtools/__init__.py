"""typeformtools - Tools for PEP 747 `TypeForm`s - Olaf, 16 Dec 2024-21 Apr 2025.

Module `typeformtools` provides various helper functions to ease overcoming
[challenges](https://peps.python.org/pep-0747/#challenges-when-accepting-all-typeforms) posed by PEP 747 `TypeForm`s.

See [PEP 747](https://peps.python.org/pep-0747/) for the `TypeForm` type annotation for type expression results.
Note this is *unrelated* to the similarly named [Typeform](https://www.typeform.com/) online forms / survey SaaS.

This *work in progress* version currently offers:

* `unaliased()` to resolve `type =` aliases (if applicable)

        >>> type X = int
        >>> assert X is not str and unaliased(X) is int

    One useful example of use is `isinstance()`, which will
    [*not* support type aliases](https://discuss.python.org/t/run-time-behaviour-of-typealiastype/43774/29)

        >>> type BuiltInNumber = int | float | complex
        >>> # noinspection PyUnresolvedReferences
        ... assert all(isinstance(nr, unaliased(BuiltInNumber)) for nr in (42, 3.14, -1j))

* `unannotated()` to remove the annotation (if applicable)

        >>> X = Annotated[int, "annotation"]
        >>> assert X is not int and unannotated(X) is int

* `undisguised()` to combine the above two (if applicable)

        >>> type X = Annotated[int, "annotation"]
        >>> assert X is not int and undisguised(X) is int

* `non_optional()` to remove optionality in a union (if applicable)

        >>> X = int | None
        >>> assert X is not int and non_optional(X) is int

    A possible example scenario, which triggered including this, is conversion between type definitions:
    * in **Python** (cannot be `None` unless *allowed*)
    * and in **SQL** (can be `NULL` unless *forbidden*)

* `literal_values()` to get `Literal[...]` `TypeForm`'s values

    >>> literal_values(Literal[1, 'two', None])
    (1, 'two', None)
"""
import datetime
import enum
import functools
import logging
import operator
from collections.abc import Iterable, Iterator, Sequence, Sized
from types import NoneType, UnionType
# noinspection PyUnresolvedReferences,PyProtectedMember
from typing import _AnnotatedAlias, _LiteralGenericAlias, _SpecialForm, _UnionGenericAlias
from typing import Annotated, cast, get_args, get_origin, Literal, Never, Optional, TypeAliasType, Union

import more_itertools
# noinspection PyUnresolvedReferences,PyProtectedMember
from typing_extensions import Doc, TypeForm


__all__ = ['unaliased', 'unannotated', 'undisguised', 'non_optional', 'literal_values']

logger = logging.getLogger(__name__)


# --- helper
def _union[T, U](types: Iterable[type[T] | TypeForm[T]]) -> type[U] | TypeForm[U] | Never:
    """Return union of 0, 1, or more `types`.

    0 `types` results in `Never`, 1 single type in that type, more `types` in a union
    >>> assert _union([]) is Never and _union([int]) is int and _union([int, str]) == int | str
    """
    # TODO flatten so _union(int | str, bool) == int | str | bool
    # TODO deduplicate so _union(int, str, int) == int | str

    if not isinstance(types, Sized):
        types = tuple(types)
    return functools.reduce(operator.or_, types) if types else Never


# --- TypeForm tools
def unaliased[T](tf: TypeAliasType | type[T] | TypeForm[T]) -> type[T] | TypeForm[T]:
    """Return (ultimate) target type(form) of `tf` if it's (potentially indirect) type alias, else `tf` unchanged.

    >>> type IntAlias = int
    >>> type IntAliasAlias = IntAlias
    >>> type IntAliasAliasALias = IntAliasAlias
    >>> for test in int, IntAlias, IntAliasAlias, IntAliasAliasALias:
    ...     assert unaliased(test) is int, test

    >>> assert unaliased(list[IntAlias]) == list[int]  # TODO see below # doctest: +SKIP
    >>> assert unaliased(IntAlias | str) == int | str  # TODO see below # doctest: +SKIP
    """
    # TODO make `if (origin := get_origin(tf)) is not None: return origin[*map(unaliased, get_args(tf))]` working

    while isinstance(tf, TypeAliasType):      # loop for (indirect) `type` aliases
        logger.debug(f"type {tf.__name__} = {tf.__value__}")
        tf = tf.__value__                     # remove one level of `type`
    assert not isinstance(tf, TypeAliasType)  # state the obvious to type checkers
    return tf


def unannotated[T](tf: type[Annotated[T, ...]] | _AnnotatedAlias | type[T] | TypeForm[T]) -> type[T] | TypeForm[T]:
    """Return type(form) `tf` without annotations if it's `Annotated[...]`, else `tf` unchanged.

    >>> for test in int, Annotated[int, 'annotation'], Annotated[Annotated[int, 'annotation'], ...]:
    ...     assert unannotated(test) is int, test
    """
    # TODO handle *composed* `TypeForm`s like in `unaliased()`

    if isinstance(tf, _AnnotatedAlias):         # no need for loop as nested `Annotated`'s are flattened
        logger.debug(f"Annotated[{tf.__origin__}, ...]")
        tf = tf.__origin__                      # remove only level of `Annotated`
    assert not isinstance(tf, _AnnotatedAlias)  # state the obvious to type checkers
    return tf


def undisguised[T](tf: TypeAliasType | type[Annotated[T, ...]] | _AnnotatedAlias | type[T] | TypeForm[T]
                   ) -> type[T] | TypeForm[T]:
    """Return type(form) `tf` without (possibly multiple layers of) "disguises" (type aliases and annotations) (if any).

    >>> type IntAlias = Annotated[int, 'int']
    >>> type IntAliasAlias = Annotated[IntAlias, 'IntAlias']
    >>> type IntAliasAliasALias = Annotated[IntAliasAlias, 'IntAliasAlias']
    >>> for test in int, IntAlias, IntAliasAlias, IntAliasAliasALias:
    ...     assert undisguised(test) is int, test
    """
    # TODO handle *composed* `TypeForm`s like in `unaliased()`

    while isinstance(tf, TypeAliasType | _AnnotatedAlias):      # loop for interleaved "disguises"
        logger.debug(f"remove disguise from {tf}")
        tf = unannotated(unaliased(tf))                         # remove one or two levels of "disguise"
    assert not isinstance(tf, TypeAliasType | _AnnotatedAlias)  # state the obvious to `mypy`
    return tf


def non_optional[T](tf: (type[T | None] | UnionType | TypeForm[T | None] | type[Optional[T]] | _UnionGenericAlias
                         | TypeForm[Optional[T]] | type[T] | TypeForm[T])) -> type[T] | TypeForm[T] | Never:
    """Return type (form) `tf` without `None` optionality.

    >>> for test in int | str, int, NoneType:
    ...     assert non_optional(test | None) == (Never if test is NoneType else test), test | None
    ...     assert non_optional(Optional[test]) == (Never if test is NoneType else test), Optional[test]
    """
    def none_not_none[T](iterable: Iterable[T]) -> tuple[Iterator[T], Iterator[T]]:
        """Return `iterable` elements partitioned into those that are `None` or `NoneType`, and those that are not."""
        def is_not_none(arg: object) -> bool:
            """Return `False` iff arg is `None` or `NoneType`."""
            return undisguised(arg) not in {None, NoneType}

        return more_itertools.partition(is_not_none, iterable)

    undisguised_tf = undisguised(tf)
    if undisguised_tf in {None, NoneType}:                          # special case
        logger.debug(f"remove optionality from {tf} is {Never}")
        return Never                                                # `NoneType` without `None` is empty type

    if isinstance(undisguised_tf, _UnionGenericAlias | UnionType):  # old/new-style union with potentially `None`
        none, not_none = none_not_none(undisguised_tf.__args__)     # partition for `None` and `not None`
        if tuple(none):                                             # union includes (at least one) `None`
            logger.debug(f"remove optionality from {tf}")
            return _union(not_none)                                 # new union without `None`

    return tf                                                       # otherwise nothing changes


def literal_values[T](tf: _LiteralGenericAlias | type[T] | TypeForm[T]
                      ) -> Sequence[str | bytes | int | bool | enum.Enum | None]:
    """Return literal values making up `Literal` `tf` (or fail for other kind of `tf`).

    >>> literal_values(Annotated[Literal[1, 'two'], "1 or 2"])
    (1, 'two')
    """
    tf = undisguised(tf)
    if not isinstance(tf, _LiteralGenericAlias):
        raise TypeError(f"{tf} is not a parametrised Literal[...]")
    assert isinstance(tf, _LiteralGenericAlias)  # state the obvious to type checkers
    logger.debug(f"Literal[{', '.join(map(repr, tf.__args__))}]")
    return tf.__args__


if datetime.date.today() == 'Hell freezes over':
    # TODO complete simplify, consider specific sort to prevent `O(n**2)`
    def simplify[T, U](tf: type[T | U] | TypeForm[T | U] | type[T] | TypeForm[T]) -> type[T] | TypeForm[T] | Never:
        """
        >>> assert simplify(int | str | int | bool) == int | str  # remove duplicates and subclasses
        """
        def non_subclasses[T](types: Iterable[type[T] | TypeForm[T]]) -> Iterator[type[T] | TypeForm[T]]:
            """
            >>> assert set(non_subclasses([int, str, int, bool])) == {int, str}
            """
            types = set(map(unaliased, map(unannotated, types)))
            for cls in types:
                others = tuple(types - {cls})
                if not issubclass(cls, cast(tuple[type, ...], others)):
                    yield cls

        tf = unaliased(unannotated(tf))
        if tf in {None, type(None)}:
            return Never
        if get_origin(tf) not in {UnionType, Union}:
            return tf

        return _union(non_subclasses(get_args(tf)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
