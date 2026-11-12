"""
Example module
"""
from dataclasses import dataclass


@dataclass
class Point:
    """
    A Point

    Attributes
    ----------
    x: int
        The x value
    y: str
        The y value
    """
    x: int
    """X value"""
    y: str
    """Y value"""


def deprecated_function():
    """
    Some old function.

    .. deprecated:: 3.1
       Use :func:`other` instead.
    """
    pass


# Like builtins such as `range`, these take `*args`, so their real signature
# is only in the first docstring line (autodoc_docstring_signature).
def span(*args):
    """span([start, ]stop[, step])

    Return the numbers from start (default 0) up to stop, by step (default 1).
    """
    return list(range(*args))


def clock(*args):
    """clock([hour[, minute[, second]]])

    Format a time of day as ``HH:MM:SS``; missing parts are zero.
    """
    return ":".join(f"{part:02}" for part in (*args, 0, 0, 0)[:3])


def func1(param1: int) -> int:
    """This is a function with a single parameter.
    Thanks to github.com/remiconnesson.

    :param param1: This is a single parameter.
    """
    pass


def func2(param1: int, param2: int) -> str:
    """This is a function with two parameters.

    :param param1: This is the first parameter.
    :param param2: This is the second parameter.
    """
    pass


def func3(param1: int, param2: int):
    """This is a function with two parameters.

    :param param1: Alice [1]_.
    :param param2: Bon [2]_.

    References
    ----------
    .. [1] Alice is commonly used to describe the first actor.
    .. [2] Bob is commonly used to describe the second actor.
    """
    pass
