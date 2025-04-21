"""Useful protocols for structural subtyping."""

from typing import (
    Any,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from typing_extensions import deprecated  # TODO: Replace with typing when support for 3.12 drops


@deprecated("Use SupportsDunder[...] versions")
@runtime_checkable
class SupportsLessThan[T](Protocol):
    """Objects supporting less-than comparisons."""

    def __lt__(self, __other: T) -> bool: ...


@deprecated("Use SupportsDunder[...] versions")
@runtime_checkable
class SupportsLessOrEqual[T](Protocol):
    """Objects supporting less-or-equal comparisons."""

    def __lt__(self, __other: T) -> bool: ...


@deprecated("Use SupportsDunder[...] versions")
@runtime_checkable
class SupportsGreaterThan[T](Protocol):
    """Objects supporting greater-than comparisons."""

    def __lt__(self, __other: T) -> bool: ...


@deprecated("Use SupportsDunder[...] versions")
@runtime_checkable
class SupportsGreaterOrEqual[T](Protocol):
    """Objects supporting greater-or-equal comparisons."""

    def __lt__(self, __other: T) -> bool: ...


_T_contra = TypeVar("_T_contra", contravariant=True)

# Comparison protocols


@runtime_checkable
class SupportsDunderLT(Protocol[_T_contra]):  # noqa: D101
    def __lt__(self, other: _T_contra, /) -> bool: ...


@runtime_checkable
class SupportsDunderGT(Protocol[_T_contra]):  # noqa: D101
    def __gt__(self, other: _T_contra, /) -> bool: ...


@runtime_checkable
class SupportsDunderLE(Protocol[_T_contra]):  # noqa: D101
    def __le__(self, other: _T_contra, /) -> bool: ...


@runtime_checkable
class SupportsDunderGE(Protocol[_T_contra]):  # noqa: D101
    def __ge__(self, other: _T_contra, /) -> bool: ...


@runtime_checkable
class SupportsAllComparisons[T](  # noqa: D101
    SupportsDunderLT[T],
    SupportsDunderGT[T],
    SupportsDunderLE[T],
    SupportsDunderGE[T],
    Protocol,
): ...


type SupportsRichComparison = SupportsDunderLT[Any] | SupportsDunderGT[Any]
SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=SupportsRichComparison)
