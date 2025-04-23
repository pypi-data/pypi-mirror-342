import functools
from importlib.util import find_spec

from .utils import if_none


def _broken_func(error: str):
    raise ImportError(error)


def _get_broken_func(error: str):
    return functools.partial(_broken_func, error)


class BrokenClass:
    """Dummy class which raises an ImportError when initialized"""

    ERROR = ""

    def __init__(self, *args, **kwargs):
        raise ImportError(self.__class__.ERROR)


class OptionalModule:
    """Class used by other eo4eu modules to handle code that
    should not be called when an extension is not installed

    :param package: The name of the package
    :type package: str
    :param enabled_by: The names of extensions which enable this functionality
    :type enabled_by: list[str]
    :param depends_on: The actual Python modules needed for this functionality
    :type depends_on: list[str]
    """
    def __init__(
        self,
        package: str,
        enabled_by: list[str],
        depends_on: list[str]
    ):
        self._package = package
        self._enabled_by = enabled_by
        self._depends_on = depends_on

    def is_enabled(self) -> bool:
        """Used to check whether the submodule is enabled

        :returns: Whether the dependencies of the module exist in the system
        :rtype: bool
        """
        if len(self._depends_on) == 0:
            return True

        return all([
            find_spec(dep) is not None
            for dep in self._depends_on
        ])

    def _error_message(self, name: str) -> str:
        preamble = f"{name} is not included in the base install of {self._package}."
        if len(self._enabled_by) == 0:
            return preamble

        submodule_blurb = ""
        if len(self._enabled_by) == 1:
            submodule_blurb = f"{self._package}[{self._enabled_by[0]}]"
        else:
            head, tail = self._enabled_by[:-1], self._enabled_by[-1]
            submodule_blurb = ", ".join([
                f"{self._package}[{submodule}]"
                for submodule in head
            ]) + f" or {self._package}[{tail}]"

        return f"{preamble} Please enable using {submodule_blurb}."

    def broken_class(self, name: str, class_attrs: list[str]|None = None):
        """Creates a class which will raise a nice ImportError if anyone tries
        to initialize it

        :param name: The name of the broken class
        :type name: str
        :param class_attrs: Optional class attributes that will also raise an appropriate Import error when accessed
        :type class_attrs: list[str]|None
        :rtype: type
        """
        class_attrs = if_none(class_attrs, [])

        result = type(
            name,
            (BrokenClass,),
            {attr: _get_broken_func(self._error_message(name)) for attr in class_attrs}
        )
        result.ERROR = self._error_message(name)
        return result

    def broken_func(self, name: str):
        """Creates a function which raises a nice ImportError when called

        :param name: The name of the broken function
        :type name: str
        :rtype: Callable
        """
        return _get_broken_func(self._error_message(name))

    def raise_error(self, name: str):
        """Raises a nice ImportError

        :param name: The name of the broken object
        :type name: str
        """
        raise ImportError(self._error_message(name))
