import numpy as np
import pytest
from numpy.testing import assert_array_equal

from kajihs_utils.numpy_utils import IncompatibleShapeError, find_closest


# TODO: Check and fix those tests
class TestFindClosest:
    def test_scalar_inputs_single_target(self):
        # x: (N,), target: scalar
        x = np.array([0, 10, 20, 30])
        target = 12
        # The closest to 12 is 10 at index 1
        result = find_closest(x, target)
        assert result == 1

    def test_scalar_inputs_multiple_targets(self):
        # x: (N,), targets: (M,)
        x = np.array([0, 10, 20, 30])
        targets = np.array([2, 26])
        # Closest to 2 is 0 at index 0, closest to 26 is 30 at index 3
        result = find_closest(x, targets)
        assert_array_equal(result, np.array([0, 3]))

    def test_vector_inputs_single_target(self):
        # x: (N, D), target: (D,)
        x = np.array([[0, 0], [10, 10], [20, 20]])
        target = np.array([6, 5])
        # Distances:
        # to [0,0] ~ sqrt(6^2+5^2)=sqrt(61)
        # to [10,10] ~ sqrt((10-6)^2+(10-5)^2)=sqrt(16+25)=sqrt(41)=closest
        # to [20,20] ~ sqrt((20-6)^2+(20-5)^2) large number
        result = find_closest(x, target)
        assert result == 1

    def test_vector_inputs_multiple_targets(self):
        # x: (N, D), targets: (M, D)
        x = np.array([[0, 0], [10, 10], [20, 20]])
        targets = np.array([[-1, -1], [15, 12]])
        # Distances to [-1,-1]:
        #   [0,0]: sqrt(1+1)=sqrt(2)
        #   [10,10]: large
        #   [20,20]: larger
        # Closest: index 0
        # Distances to [15,12]:
        #   [0,0]: sqrt(15^2+12^2)=sqrt(225+144)=sqrt(369)
        #   [10,10]: sqrt(5^2+2^2)=sqrt(29)=closest
        #   [20,20]: sqrt((20-15)^2+(20-12)^2)=sqrt(25+64)=sqrt(89)
        # Closest: index 1
        result = find_closest(x, targets)
        assert_array_equal(result, np.array([0, 1]))

    def test_matrix_inputs_single_target(self):
        # x: (N, H, W), target: (H, W)
        x = np.array([[[0, 0], [0, 0]], [[10, 10], [10, 10]], [[20, 20], [20, 20]]])
        target = np.array([[2, 2], [2, 2]])
        # Distances (fro norm):
        # to [[[0,0],[0,0]]] = sqrt(2^2+2^2+2^2+2^2)=sqrt(16)=4
        # to [[[10,10],[10,10]]] = large
        # to [[[20,20],[20,20]]] = larger
        # Closest: index 0
        result = find_closest(x, target, norm_ord="fro")
        assert result == 0

    def test_matrix_inputs_multiple_targets(self):
        # x: (N, H, W)
        x = np.array([[[0, 0], [0, 0]], [[10, 10], [10, 10]], [[20, 20], [20, 20]]])
        targets = np.array([
            [[0, 0], [1, 1]],  # close to first
            [[19, 19], [19, 19]],  # close to last
        ])
        # First target distances:
        #   to x[0]: fro sqrt(0^2+0^2+(1^2)+(1^2)=sqrt(2)=1.414..
        #   to x[1]: fro sqrt((10^2+10^2)+(9^2+9^2)) large
        #   to x[2]: even larger
        # Closest: index 0
        # Second target distances:
        #   to x[0]: big
        #   to x[1]: sqrt((9^2 four times)= sqrt(81*4)=sqrt(324)=18
        #   to x[2]: sqrt((1^2 four times)= sqrt(4)=2 closest
        # Closest: index 2
        result = find_closest(x, targets, norm_ord="fro")
        assert_array_equal(result, np.array([0, 2]))

    def test_four_dimensional_inputs(self):
        # x: (N, A, B, C) e.g. (3,2,2,2)
        x = np.array([
            np.zeros((2, 2, 2)),
            np.ones((2, 2, 2)) * 10,
            np.ones((2, 2, 2)) * 20,
        ])
        target = np.ones((2, 2, 2)) * 9
        # Flattened norms:
        # Dist to x[0]: sqrt(9^2 * 8 elements)= sqrt(81*8)= sqrt(648)
        # Dist to x[1]: sqrt((10-9)^2 * 8)= sqrt(1*8)= sqrt(8)=2.828...
        # Dist to x[2]: sqrt((20-9)^2 * 8)= large
        # Closest: index 1
        result = find_closest(x, target)
        assert result == 1

    def test_multiple_targets_for_four_dimensional(self):
        x = np.array([
            np.zeros((2, 2, 2)),
            np.ones((2, 2, 2)) * 10,
            np.ones((2, 2, 2)) * 20,
        ])
        targets = np.array([
            np.ones((2, 2, 2)),  # closer to 0 (distance large) or 10?
            np.ones((2, 2, 2)) * 15,  # closer to 10 or 20?
        ])
        # For target ~1:
        # Dist to x[0]: sqrt((1-0)^2 *8)= sqrt(1*8)= sqrt(8)
        # Dist to x[1]: sqrt((10-1)^2 *8)= sqrt(81*8)=sqrt(648)
        # Dist to x[2]: sqrt((20-1)^2 *8)= even bigger
        # Closest: index 0
        # For target ~15:
        # Dist to x[0]: sqrt(15^2*8) large
        # Dist to x[1]: sqrt((10-15)^2*8)= sqrt(25*8)= sqrt(200)
        # Dist to x[2]: sqrt((20-15)^2*8)= sqrt(25*8)= sqrt(200)
        # Ties between index 1 and 2, np.argmin returns the first min, so index 1.
        result = find_closest(x, targets)
        assert_array_equal(result, np.array([0, 1]))

    def test_single_target_same_shape_returns_int(self):
        x = np.array([[0, 1], [2, 3], [4, 5]])
        target = np.array([3, 4])
        # This should return a single integer because target is the same shape as an element
        result = find_closest(x, target)
        assert isinstance(result, np.integer)

    def test_multiple_targets_return_array(self):
        x = np.array([[0, 1], [2, 3], [4, 5]])
        targets = np.array([[1, 1], [3, 3]])
        # This should return an array because we have multiple targets
        result = find_closest(x, targets)
        assert isinstance(result, np.ndarray)
        assert result.shape == (2,)

    def test_incompatible_shape_error_single_target(self):
        x = np.array([[0, 10, 20], [30, 40, 50]])  # shape (4,)
        target = np.array([1, 2])  # shape (2,) incompatible with (N,) elements
        with pytest.raises(IncompatibleShapeError):
            find_closest(x, target)

    def test_incompatible_shape_error_multiple_targets(self):
        x = np.array([[0, 0], [1, 1], [2, 2]])  # shape (3,2)
        targets = np.array([[0], [1]])  # shape (2,1), incompatible with (2,)
        with pytest.raises(IncompatibleShapeError):
            find_closest(x, targets)

    def test_norm_ord_none(self):
        # Check that passing norm_ord=None is acceptable and uses default norm (2-norm)
        x = np.array([[0, 0], [10, 10], [20, 20]])
        target = np.array([6, 5])
        result_default = find_closest(x, target, norm_ord=None)
        result_2 = find_closest(x, target, norm_ord=2)
        assert result_default == result_2

    def test_invalid_norm_ord_for_non_matrix_with_fro(self):
        # "fro" norm is defined for matrices (2D), but let's see if it raises an error for vectors.
        x = np.array([0, 10, 20, 30])  # shape (4,), scalar dimension
        target = 12
        # numpy.linalg.norm with 'fro' and 1D array works but treats it as a 2D array with shape (4,1)
        # which leads to a ValueError because 'fro' is only defined for 2D matrices.
        # We can test if this raises a ValueError.
        with pytest.raises(ValueError):
            find_closest(x, target, norm_ord="fro")

    def test_invalid_norm_ord_for_non_matrix_with_nuc(self):
        # "nuc" norm (nuclear norm) is only defined for 2D arrays.
        # Here we test with a 1D array and expect a ValueError.
        x = np.array([0, 10, 20, 30])
        target = 12
        with pytest.raises(ValueError):
            find_closest(x, target, norm_ord="nuc")

    def test_nuc_norm_for_2d_arrays(self):
        x2 = np.array([[[0, 0]], [[10, 10]], [[20, 20]]])  # shape (3, 1, 2)
        target2 = np.array([[6, 5]])  # shape (1,2)
        result = find_closest(x2, target2, norm_ord="nuc")
        # Should return a single index
        assert result == 1

    def test_custom_norm_ord_int(self):
        # Test a custom integer norm (like 1-norm)
        x = np.array([[0, 0], [10, 10], [20, 20]])
        target = np.array([6, 5])
        # With 1-norm:
        # Distances:
        # to [0,0]: |6|+|5|=11
        # to [10,10]: |10-6|+|10-5|=4+5=9 closest
        # to [20,20]: big
        result = find_closest(x, target, norm_ord=1)
        assert result == 1

    def test_multiple_targets_and_int_norm(self):
        x = np.array([[0, 0], [10, 10], [20, 20]])
        targets = np.array([[1, 1], [15, 15]])
        # With 1-norm:
        # For [1,1]:
        #   to [0,0]: sum(|1|+|1|)=2
        #   to [10,10]: sum(|9|+|9|)=18
        #   to [20,20]: sum(|19|+|19|)=38
        # closest: 0
        # For [15,15]:
        #   to [0,0]: sum(|15|+|15|)=30
        #   to [10,10]: sum(|5|+|5|)=10
        #   to [20,20]: sum(|5|+|5|)=10 tie, argmin picks first: index 1
        result = find_closest(x, targets, norm_ord=1)
        assert_array_equal(result, [0, 1])
