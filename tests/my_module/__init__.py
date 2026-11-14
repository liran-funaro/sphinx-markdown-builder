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


def downside_risk(returns, min_acceptable_return=0.0):
    """
    Compute the downside risk of a series of returns.

    Parameters
    ----------
    returns : ndarray of shape (n_observations,)
        The observed returns.
    min_acceptable_return : float, optional
        Returns below this value count as downside.

    Returns
    -------
    risk : float
        The downside risk.
    """
    return 0.0
