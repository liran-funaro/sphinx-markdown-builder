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


def func1(param1: int):
    """This is a function with a single parameter.
    Thanks to github.com/remiconnesson.

    :param param1: This is a single parameter.
    """
    pass


def func2(param1: int, param2: int):
    """This is a function with two parameters.

    :param param1: This is the first parameter.
    :param param2: This is the second parameter.
    """
    pass


def func3(param1: int, param2: int):
    """This is a function with two parameters.

    :param param1: This is the first parameter [1]_.
    :param param2: This [2]_ is the second parameter.

    References
    ----------
    .. [1] `Google <https://google.com>`_
    .. [2] `Github <https://github.com>`_
    """
    pass
