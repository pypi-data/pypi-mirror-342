"""
Utils for arithmetic.

close_factors and almost_factors taken from:
https://code.visualstudio.com/api/language-extensions/semantic-highlight-guide
"""


def closest_factors(n: int, /) -> tuple[int, int]:
    """
    Find the closest pair of factors.

    Args:
        n: The number to find factors for.

    Returns:
        A tuple containing the two closest factors of n, the larger first.

    Example:
        >>> closest_factors(99)
        (11, 9)
    """
    factor1 = 0
    factor2 = n
    while factor1 + 1 <= factor2:
        factor1 += 1
        if n % factor1 == 0:
            factor2 = n // factor1

    return factor1, factor2


def almost_factors(n: int, /, ratio: float = 0.5) -> tuple[int, int]:
    """
    Find a pair of factors that are close enough.

    Args:
        n: The number to almost-factorize.
        ratio: The threshold ratio between both factors.

    Returns:
        A tuple containing the first two numbers factoring to n or more such
        that factor 1 is at most 1/ratio times larger than factor 2.

    Example:
        >>> almost_factors(10, ratio=0.5)
        (4, 3)
    """
    while True:
        factor1, factor2 = closest_factors(n)
        if ratio * factor1 <= factor2:
            break
        n += 1
    return factor1, factor2
