"""
A module class file.
"""
from typing import Optional, overload

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

    @overload
    def create(self, *, username: str, email: str) -> str:
        """Create by username and email"""

    @overload
    def create(self, *, job_id: str) -> int:
        """Create by job id"""

    def create(self, *, username: Optional[str] = None, email: Optional[str] = None, job_id: Optional[str] = None):
        """Create something with keyword-only arguments"""
        return job_id if username is None else f"{username}:{email}"
