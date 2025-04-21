from math import isclose

from kajihs_utils.numpy_utils import Vec2d

ABS_TOL = 1e-12


def test_vec2d_creation():
    v = Vec2d(3.0, 4.0)
    assert isinstance(v, Vec2d)
    assert isclose(v.x, 3.0)
    assert isclose(v.y, 4.0)


def test_x_property():
    v = Vec2d(3.0, 4.0)
    assert isclose(v.x, 3.0)
    v.x = 5.0
    assert isclose(v.x, 5.0)


def test_y_property():
    v = Vec2d(3.0, 4.0)
    assert isclose(v.y, 4.0)
    v.y = 6.0
    assert isclose(v.y, 6.0)


def test_magnitude():
    v = Vec2d(3.0, 4.0)
    assert isclose(v.magnitude(), 5.0)  # Magnitude of (3, 4) is 5
    v_zero = Vec2d(0.0, 0.0)
    assert isclose(v_zero.magnitude(), 0.0)


def test_normalized():
    v = Vec2d(3.0, 4.0)
    normalized_v = v.normalized()
    assert isclose(normalized_v.magnitude(), 1.0)
    assert isclose(normalized_v.x, 3 / 5)
    assert isclose(normalized_v.y, 4 / 5)

    v_zero = Vec2d(0.0, 0.0)
    normalized_v_zero = v_zero.normalized()
    assert isclose(normalized_v_zero.x, 0.0)
    assert isclose(normalized_v_zero.y, 0.0)


def test_angle():
    v = Vec2d(1.0, 0.0)
    assert isclose(v.angle(), 0.0)  # Angle of (1, 0) is 0 degrees
    v2 = Vec2d(0.0, 1.0)
    assert isclose(v2.angle(), 90.0)  # Angle of (0, 1) is 90 degrees
    v3 = Vec2d(-1.0, 0.0)
    assert isclose(v3.angle(), 180.0)  # Angle of (-1, 0) is 180 degrees
    v4 = Vec2d(0.0, -1.0)
    assert isclose(v4.angle(), -90.0)  # Angle of (0, -1) is -90 degrees


def test_rotate():
    # Vector to rotate
    v = Vec2d(1.0, 0.0)

    # Rotate around the origin (0, 0), expected result after 90 degrees counterclockwise: (0, 1)
    rotated_v = v.rotate(90.0)
    assert isclose(rotated_v.x, 0.0, abs_tol=ABS_TOL)
    assert isclose(rotated_v.y, 1.0)

    # Rotate around the origin (0, 0), expected result after 180 degrees: (-1, 0)
    rotated_v_180 = v.rotate(180.0)
    assert isclose(rotated_v_180.x, -1.0)
    assert isclose(rotated_v_180.y, 0.0, abs_tol=ABS_TOL)

    # Rotate around a new center (cx=1, cy=1), expected result after 90 degrees counterclockwise
    # First, translate the vector to origin (1, 1), rotate, then translate back to (1, 1)
    v = Vec2d(2.0, 0.0)
    rotated_v_center = v.rotate(90.0, (1.0, 1.0))  # Rotate around (1, 1)
    assert isclose(rotated_v_center.x, 2.0)
    assert isclose(rotated_v_center.y, 2.0)

    # Rotate around the new center (cx=1, cy=1), expected result after 180 degrees: (0, 1)
    rotated_v_center_180 = v.rotate(180.0, (1.0, 1.0))
    assert isclose(rotated_v_center_180.x, 0.0, abs_tol=ABS_TOL)
    assert isclose(rotated_v_center_180.y, 2.0)


def test_repr():
    v = Vec2d(1.234, 5.678)
    assert repr(v) == "Vec2d(1.23, 5.68)"  # Test that it formats to 2 decimal places
