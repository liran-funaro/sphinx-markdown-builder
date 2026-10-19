"""
A module class file.
"""
from .submodule.my_class import SubmoduleClass

default_var = "some_default_value"
"""A default variable to be used by :py:class:`SubmoduleClass`"""


class ModuleClass:
    """
    A class inside a module.
    """

    def __init__(self):
        """Initialize a module class object"""
        self.submodule_class = SubmoduleClass(default_var)

    def function(self, param1: int, param2: str) -> None:
        """Do nothing

        This is a dummy function that does not do anything.

        :param param1: Does nothing
        :type param1: int
        :param param2: Does nothing as well
        :type param2: str
        :return: Nothing.
        :rtype: None

        .. seealso::
           :py:meth:`~my_module.submodule.my_class.SubmoduleClass.function`
        """
        self.submodule_class.function(param1, param2)

    def optional_params(self, *args):
        """optional_params(a[, b[, c]])

        A function with optional parameters.
        """
