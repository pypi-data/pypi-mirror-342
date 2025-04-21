"""Tools for numpy."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, override

import numpy as np
from numpy import dtype, float64, floating, int_, ndarray

if TYPE_CHECKING:
    from collections.abc import Iterable

    from numpy.typing import ArrayLike, NDArray

type Norm = float | Literal["fro", "nuc"]
type AnyFloat = float | float64


class IncompatibleShapeError(ValueError):
    """Shapes of input arrays are incompatible for a given function."""

    def __init__(self, arr1: NDArray[Any], arr2: NDArray[Any], obj: Any) -> None:
        super().__init__(
            f"Shapes of inputs arrays {arr1.shape} and {arr2.shape} are incompatible for {obj.__name__}"
        )


# TODO: Add axis parameters
def find_closest[T](
    x: Iterable[T] | ArrayLike,
    targets: Iterable[T] | T | ArrayLike,
    norm_ord: Norm | None = None,
) -> ndarray[tuple[int], dtype[int_]] | int_:
    """
    Find the index of the closest element(s) from `x` for each target in `targets`.

    Given one or multiple `targets` (vectors vectors or scalars),
    this function computes the distance to each element in `x` and returns the
    indices of the closest matches. If `targets` is of the same shape as an
    element of `x`, the function returns a single integer index. If `targets`
    contains multiple elements, it returns an array of indices corresponding to
    each target.

    If the dimensionality of the vectors in `x` is greater than 2, the vectors
    will be flattened into 1D before computing distances.

    Args:
        x: An iterable or array-like collection of elements (scalars, vectors,
            or higher-dimensional arrays). For example, `x` could be an array of
            shape `(N,)` (scalars), `(N, D)` (D-dimensional vectors),
            `(N, H, W)` (2D arrays), or higher-dimensional arrays.
        targets: One or multiple target elements for which you want to find the
            closest match in `x`. Can be a single scalar/vector/array or an
            iterable of them.
            Must be shape-compatible with the elements of `x`.
        norm_ord: The order of the norm used for distance computation.
            Uses the same conventions as `numpy.linalg.norm`.

    Returns:
        An array of indices. If a single target was given, a single index is
        returned. If multiple targets were given, an array of shape `(M,)` is
        returned, where `M` is the number of target elements. Each value is the
        index of the closest element in `x` to the corresponding target.

    Raises:
        IncompatibleShapeError: If `targets` cannot be broadcast or reshaped to
            match the shape structure of the elements in `x`.

    Examples:
        >>> import numpy as np
        >>> x = np.array([0, 10, 20, 30])
        >>> int(find_closest(x, 12))
        1
        >>> # Multiple targets
        >>> find_closest(x, [2, 26])
        array([0, 3])

        >>> # Using vectors
        >>> x = np.array([[0, 0], [10, 10], [20, 20]])
        >>> int(find_closest(x, [6, 5]))  # Single target vector
        1
        >>> find_closest(x, [[-1, -1], [15, 12]])  # Multiple target vectors
        array([0, 1])

        >>> # Higher dimensional arrays
        >>> x = np.array([[[0, 0], [0, 0]], [[10, 10], [10, 10]], [[20, 20], [20, 20]]])
        >>> int(find_closest(x, [[2, 2], [2, 2]]))
        0
        >>> find_closest(x, [[[0, 0], [1, 1]], [[19, 19], [19, 19]]])
        array([0, 2])
    """
    x = np.array(x)  # (N, vector_shape)
    targets = np.array(targets)
    vector_shape = x.shape[1:]

    # Check that shapes are compatible
    do_unsqueeze = False
    if targets.shape == vector_shape:
        targets = np.atleast_1d(targets)[np.newaxis, :]  # (M, vector_shape)
        do_unsqueeze = True
    elif targets.shape[1:] != vector_shape:
        raise IncompatibleShapeError(x, targets, find_closest)

    nb_vectors = x.shape[0]  # N
    nb_targets = targets.shape[0]  # M

    diffs = x[:, np.newaxis] - targets

    match vector_shape:
        case ():
            distances = np.linalg.norm(diffs[:, np.newaxis], ord=norm_ord, axis=1)
        case (_,):
            distances = np.linalg.norm(diffs, ord=norm_ord, axis=2)
        case (_, _):
            distances = np.linalg.norm(diffs, ord=norm_ord, axis=(2, 3))
        case _:  # Tensors
            # Reshape to 1d vectors
            diffs = diffs.reshape(nb_vectors, nb_targets, -1)
            distances = np.linalg.norm(diffs, ord=norm_ord, axis=2)

    closest_indices = np.argmin(distances, axis=0)
    if do_unsqueeze:
        closest_indices = closest_indices[0]

    return closest_indices


class Vec2d(ndarray[Literal[2], dtype[float64]]):
    """A 2D vector subclassing numpy.ndarray with .x and .y properties."""

    def __new__(cls, x: AnyFloat, y: AnyFloat) -> Vec2d:  # noqa: D102
        obj = np.asarray([x, y], dtype=np.float64).view(cls)
        return obj

    @property
    def x(self) -> float:
        """X coordinate."""
        return self[0]

    @x.setter
    def x(self, value: float) -> None:
        self[0] = value

    @property
    def y(self) -> float:
        """Y coordinate."""
        return self[1]

    @y.setter
    def y(self, value: float) -> None:
        self[1] = value

    def magnitude(self) -> floating[Any]:
        """Magnitude or norm of the vector."""
        return np.linalg.norm(self)

    def normalized(self) -> Vec2d:
        """Return a normalized version of the vector."""
        mag = self.magnitude()
        return self if mag == 0 else Vec2d(self.x / mag, self.y / mag)

    def angle(self) -> float:
        """Return the angle (in degrees) between the vector and the positive x-axis."""
        return np.degrees(np.arctan2(self.y, self.x))

    def rotate(self, degrees_angle: float, center: tuple[float, float] = (0, 0)) -> Vec2d:
        """Rotates the vector counterclockwise by a given angle (in degrees) around the point (cx, cy)."""
        cx, cy = center[0], center[1]
        # Step 1: Translate the vector to the origin (subtract the center of rotation)
        translated_x = self.x - cx
        translated_y = self.y - cy

        # Step 2: Rotate the translated vector
        rad = np.radians(degrees_angle)
        rot_matrix = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
        rotated_vector = rot_matrix @ np.array([translated_x, translated_y])

        # Step 3: Translate the vector back to its original position
        new_x = rotated_vector[0] + cx
        new_y = rotated_vector[1] + cy

        return Vec2d(new_x, new_y)

    @override
    def __repr__(self) -> str:
        return f"Vec2d({self.x:.2f}, {self.y:.2f})"
