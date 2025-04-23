from .typing import Any


def if_none(value: Any, default: Any):
    """This is literally `default` if `value` is None else `value`

    :param value: The value to return if not None
    :type value: Any
    :param default: The value to return if None
    :type default: Any
    :rtype: Any
    """
    return default if value is None else value
