from kajihs_utils import get_first, is_sorted
from kajihs_utils.loguru import prompt, setup_logging
from kajihs_utils.numpy_utils import Vec2d, find_closest

# Useful protocols for structural subtyping
from kajihs_utils.protocols import SupportsAllComparisons, SupportsDunderLT

# Get first key existing in a dict
d = {"a": 1, "b": 2, "c": 3}
print(get_first(d, ["x", "a", "b"]))

# Check if an iterable is sorted
print(is_sorted([1, 2, 2, 3]))
print(is_sorted("cba", reverse=True))
print(is_sorted([0, 1, 0]))

# === Loguru features ===
# Better logged and formatted prompts
prompt("Enter a number")  # snippet: no-exec

# Simply setup well formatted logging in files and console
setup_logging(prefix="app", log_dir="logs")

# === Numpy features ===
import numpy as np

x = np.array([[0, 0], [10, 10], [20, 20]])
print(find_closest(x, [[-1, 2], [15, 12]]))

# Vec2d class
v = Vec2d(3.0, 4.0)
print(v)
print(tuple(v))
print(v.x)
print(v.y)
print(v.magnitude())
print(v.normalized())
print(v.angle())
print(v.rotate(90, center=(1, 1)))
