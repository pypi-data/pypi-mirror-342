import logging
import traceback

from ..typing import Self, Any, List, Callable, TypeVar, Iterator


class Result:
    """Generic single value container type, similar to Rust's Result

    :param is_ok: Whether or not the value can be used (no unhandled errors have occured)
    :type is_ok: bool
    :param value: The value held by the container
    :type value: Any
    :param stack: A list of the errors (handled or unhandled) that have occured so far
    :type stack: List[str]
    """
    PRINT_EXCEPTIONS = False
    NDASH = 25

    def __init__(self, is_ok: bool, value: Any, stack: List[str]):
        """Initializer"""
        self._is_ok = is_ok
        self._value = value
        self._stack = stack

    @classmethod
    def none(cls) -> Self:
        """Makes empty result type (is_ok = False, value = None)

        :returns: Result.err(None)
        :rtype: Result
        """
        return Result(is_ok = False, value = None, stack = [])

    @classmethod
    def ok(cls, value: Any, stack: List[str]|None = None) -> Self:
        """Wraps the value, indicating everything is OK

        :param value: The value to return
        :type value: Any
        :param stack: Optional stack of errors (in this context treated as warnings)
        :type stack: List[str]|None
        :returns: The wrapped value
        :rtype: Result
        """
        if stack is None:
            stack = []
        return Result(is_ok = True, value = value, stack = stack)

    @classmethod
    def err(cls, error: str|List[str], value: Any = None) -> Self:
        """Wraps the error, indicating there is an unhandled error

        :param error: The unhandled error(s)
        :type value: str|List[str]
        :param value: Optional value to add to the container
        :type value: Any
        :returns: The wrapped value and error(s)
        :rtype: Result
        """
        stack = error
        if not isinstance(error, list):
            stack = [error]
        if cls.PRINT_EXCEPTIONS:
            fmt_exc = traceback.format_exc()
            if fmt_exc != "NoneType: None":
                stack[-1] += "\n".join([
                    f"\n{cls.NDASH*'-'} BEGIN EXCEPTION {cls.NDASH*'-'}",
                    fmt_exc,
                    f"{cls.NDASH*'-'}- END EXCEPTION -{cls.NDASH*'-'}\n",
                ])
        return Result(is_ok = False, value = value, stack = stack)

    @classmethod
    def wrap(self, func: Callable[[Any],Any], *args, **kwargs) -> Self:
        """Wraps a function call, returning Result.ok normally and
        Result.err if an exception is raised

        :param func: The function to call
        :type func: Callable[[Any],Any]
        :param args: the arguments to pass into the function call
        :type args: tuple[Any]
        :param kwargs: the keyword arguments to pass into the function call
        :type kwargs: Dict[str,Any]
        :returns: The wrapped result of the function call and any error(s)
        :rtype: Result
        """
        try:
            return Result.ok(func(*args, **kwargs))
        except Exception as e:
            return Result.err(str(e))

    @classmethod
    def merge_all(self, input: Iterator[Self]) -> Self:
        """Converts a list of Result values into a Result wrapping a list
        of their contents. Returns a Result.ok([values]) if all in the list are
        Result.ok or Result.err(first wrong value) if any of them are Result.err

        :param input: An iterator of Result objects
        :type input: Iterator[Result]
        :returns: Result wrapping merged iterator
        :rtype: Result
        """
        result = []
        for item in input:
            if item.is_err():
                return item
            result.append(item.get())
        return Result.ok(result)

    @classmethod
    def merge_any(self, input: Iterator[Self]) -> Self:
        """Converts a list of Result values into a Result wrapping a list
        of their contents. Returns a Result.ok([values]) if at least one
        of the items in the list are Result.ok or Result.err if all of them
        are Result.err

        :param input: An iterator of Result objects
        :type input: Iterator[Result]
        :returns: Result wrapping merged iterator
        :rtype: Result
        """
        result = []
        stack = []
        for item in input:
            if item.is_ok():
                result.append(item.get())
            else:
                stack.extend(item.stack())

        if len(result) == 0:
            return Result.err(stack)
        else:
            return Result.ok(result)

    def is_ok(self) -> bool:
        """Tells whether the value is OK

        :rtype: bool
        """
        return self._is_ok

    def is_err(self) -> bool:
        """Tells whether the value has unhandled errors

        :rtype: bool
        """
        return not self._is_ok

    def stack(self) -> List[str]:
        """Gives the stack of previous errors/warnings

        :rtype: List[str]
        """
        return self._stack

    def copy(self) -> Self:
        """Creates a new result, same as this one

        :rtype: Result
        """
        return Result(self.is_ok(), self.get(), self.stack())

    def log(self, logger: logging.Logger, level: int = logging.WARNING) -> Self:
        """Logs all warnings in the result's stack using the provided
        logger and log level

        :param logger: A standard Python logger
        :type logger: :class:`logging.Logger`
        :param level: The log level of the messages (default: logging.WARNING)
        :type level: int

        :returns: Itself, without any modifications
        :rtype: Result
        """
        for msg in self._stack:
            logger.log(level, msg)
        return self

    def then(self, other: Self) -> Self:
        """Combines two results, favoring the second value. In essence, 
        returns `other` but with this result's stack added to its stack

        :param other: The new Result
        :type other: Result
        :returns: `other` with `self`'s stack added to it
        :rtype: Result
        """
        return Result(
            is_ok = other.is_ok(),
            value = other.get(),
            stack = self._stack + other._stack
        )

    def then_ok(self, value: Any) -> Self:
        """Returns Result.ok(`value`) with this Result's stack added to
        its stack

        :param value: The new value
        :type value: Any
        :returns: Result.ok(`value`) with `self`'s stack added to it
        :rtype: Result
        """
        return self.then(Result.ok(value))

    def then_err(self, error: str|List[str], value: Any = None) -> Self:
        """Returns Result.err(`error`) with this Result's stack added to
        its stack

        :param error: The error(s) to add
        :type error: str|List[str]
        :param value: Optional value to wrap
        :type value: Any
        :returns: Result.err(`error`, `value`) with `self`'s stack added to it
        :rtype: Result
        """
        if value is None:
            value = self.get()
        return self.then(Result.err(error, value = value))

    def then_try(self, other: Self) -> Self:
        """Tries to combine `other` with `self`, but only if `other`
        is OK

        :param other: The new Result
        :type other: Result
        :returns: `self`.then(`other`) if `other` is OK, otherwise `self`
        :rtype: Result
        """
        if other.is_ok():
            return self.then(other)
        else:
            return self

    def then_warn(self, *errors: str) -> Self:
        """adds args to this Result's stack

        :param errors: The errors to add
        :type errors: tuple[str]
        :rtype: Result
        """
        return Result(
            is_ok = self.is_ok(),
            value = self.get(),
            stack = self._stack + list(errors)
        )

    def default(self, default: Any) -> Self:
        """Makes this result OK in case it's not by placing `default`
        in it

        :param default: The default value to wrap
        :type default: Any
        :returns: `self` if `self` is OK, else Result.ok(`default`)
        :rtype: Result
        """
        if self.is_err():
            return Result.ok(default)
        return self

    def pop_warning(self) -> tuple[Self,str|None]:
        """Pops the last warning off this Result's stack

        :returns: a tuple containing a Result without the warning, and the warning (or None if there are none)
        :rtype: tuple[Result,str|None]
        """
        n_warn = len(self._stack)
        if n_warn == 0:
            return self, None

        result = self.copy()
        warning = result._stack.pop(n_warn - 1)
        return result, warning

    def fmt_err(self, sep: str = "\n") -> str:
        """Returns all errors/warnings in the stack, 
        concatenated with the provided separator

        :param sep: The string to separate errors
        :type sep: str
        :rtype: str
        """
        return sep.join(self._stack)

    def get(self) -> Any:
        """Returns the value wrapped by the Result, regardless
        of whether the Result is OK

        :rtype: Any
        """
        return self._value

    def get_or(self, default: Any) -> Any:
        """Returns the value wrapped by the Result if 
        it is OK, otherwise returns `default`

        :param default: The value to return if there are unhandled errors
        :type default: Any
        :rtype: Any
        """
        if self.is_err():
            return default
        return self.get()

    def unwrap(self, exc_class: Exception = ValueError) -> Any:
        """Returns the value wrapped by the Result if 
        it is OK, otherwise raises an exception given by `exc_class`
        that contains the Result's formatted stack

        :param exc_class: The exception to raise if `self` is not OK
        :type exc_class: Exception
        :raises: `exc_class`
        :returns: The Result's contents
        :rtype: Any
        """
        if self.is_err():
            raise exc_class(self.fmt_err())
        return self.get()

    def map(self, func: Callable[Any,Any], *args, **kwargs) -> Self:
        """Returns the result of a function call, wrapped as a Result

        :param func: The function to call
        :type func: Callable[[Any],Any]
        :param args: the arguments to pass into the function call
        :type args: tuple[Any]
        :param kwargs: the keyword arguments to pass into the function call
        :type kwargs: Dict[str,Any]
        :returns: The wrapped result of the function call and any error(s), with the stack of `self` added to it
        :rtype: Result
        """
        return self.then(Result.wrap(func, *args, **kwargs))

    def map_ok(self, func: Callable[[Any],Any], *args, **kwargs) -> Self:
        """If `self` is OK, returns the wrapped function call of `func` with
        the value wrapped by `self` as its first argument, otherwise returns `self`

        :param func: The function to call
        :type func: Callable[[Any],Any]
        :param args: additional arguments to pass into the function call
        :type args: tuple[Any]
        :param kwargs: additional keyword arguments to pass into the function call
        :type kwargs: Dict[str,Any]
        :returns: The wrapped result of the function call and any error(s), with the stack of `self` added to it
        :rtype: Result
        """
        if self.is_err():
            return self
        return self.map(func, self.get(), *args, **kwargs)

    def map_err(self, func: Callable[[str],Any], *args, **kwargs) -> Self:
        """If `self` is an error, returns the wrapped function call of `func` with
        the last warning in the stack of `self`, otherwise returns `self`

        :param func: The function to call
        :type func: Callable[[Any],Any]
        :param args: additional arguments to pass into the function call
        :type args: tuple[Any]
        :param kwargs: additional keyword arguments to pass into the function call
        :type kwargs: Dict[str,Any]
        :returns: The wrapped result of the function call and any error(s), with the stack of `self` added to it
        :rtype: Result
        """
        if self.is_ok():
            return self

        result, last_warning = self.pop_warning()
        return result.map(func, last_warning, *args, **kwargs)

    def map_many(self, *funcs: Callable) -> Self:
        """Tries to apply `self`.map_ok several times, using the result of
        the previous call each time

        :param funcs: The functions to call
        :type funcs: tuple[Callable[[Any],Any]]
        :returns: The wrapped result of the function calls and any error(s)
        :rtype: Result
        """
        if self.is_err():
            return self

        result = self.copy()
        for func in funcs:
            result = result.map_ok(func)
            if result.is_err():
                break
        return result

    def map_with(self, acc: Callable[[Any,Any],Any], other: Self, *args, **kwargs) -> Self:
        """Tries to call `acc` on the values of `self` and `other`, only if they
        are both OK. Otherwise, returns whichever one is OK. If none are OK, the
        value of `other` is used. In all cases, the stacks of `self` and `other` are
        joined in the result

        :param acc: The accumulator function to combine both values
        :type acc: Callable[[Any,Any],Any]
        :param args: additional arguments to pass into the accumulator call
        :type args: tuple[Any]
        :param kwargs: additional keyword arguments to pass into the accumulator call
        :type kwargs: Dict[str,Any]
        :rtype: Result
        """
        if self.is_ok() and other.is_ok():
            return Result(
                is_ok = True,
                value = acc(self.get(), other.get(), *args, **kwargs),
                stack = self._stack + other._stack
            )
        else:
            return Result(
                is_ok = self.is_ok() or other.is_ok(),
                value = self.get() if self.is_ok() else other.get(),
                stack = self._stack + other._stack
            )

    def __repr__(self) -> str:
        """Returns the string representation of `self`

        :rtype: str
        """
        modifier = "ok" if self.is_ok() else "err"
        return f"Result.{modifier}({self.get()})"
