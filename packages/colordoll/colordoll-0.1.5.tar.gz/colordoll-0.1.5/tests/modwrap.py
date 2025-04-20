
import ast
import inspect
import astor
from typing import Any, Union, Callable, List, Dict
import logging
from types import ModuleType
import json


class ModWrapper:
    """Wraps module function calls to intercept and log them."""

    def __init__(
        self,
        _module: ModuleType,
        logger: Union[logging.Logger, None] = None,
        log_level: int = logging.INFO,
        filter_func: Union[Callable, None] = None,
    ):
        """
        Initializes ModWrapper.

        Args:
            _module     : Module to wrap.
            logger      : Logger for function calls (default: module-named logger).
            log_level   : Default logger level.
            filter_func : Optional filter for methods to wrap (takes name, returns bool).
        Raises:
            TypeError: if _module is not a ModuleType.
        """
        if not isinstance(_module, ModuleType):
            raise TypeError(f"Expected ModuleType, got {type(_module)}")

        self._module = _module
        self._name = _module.__name__
        self._logger = logger or logging.getLogger(self._name)
        self._log_level = log_level
        self._logger.setLevel(log_level)  # Ensure logger level is set.
        self._filter_func = filter_func

        self._logger.info(f"\n\nWrapping module: '{self._name}'")

    def __getattr__(self, name: str) -> Any:
        """
        Intercepts attribute access. Wraps callable attributes (functions) for logging.

        Args:
            name: Attribute name.

        Returns:
            Attribute; wrapped function if callable and filter allows, otherwise original attribute.
        """
        attr = getattr(self._module, name)
        if callable(attr) and (self._filter_func is None or self._filter_func(name)):
            return self._wrap_function(attr, name)
        return attr

    def _wrap_function(self, func: Callable, name: str) -> Callable:
        """
        Wraps a function to log calls, arguments, and return values.

        Args:
            func: The function to wrap.
            name: The name of the function.

        Returns:
            Wrapped function.
        """

        def log_and_call(*args: Any, **kwargs: Any) -> Any:
            """Inner function to log and call the original function."""
            log_level = logging.DEBUG if self._log_level <= logging.INFO and len(str(args) + str(kwargs)) < 100 else self._log_level
            log_message_header = f"Module Call: {self._name}.{name}"
            log_details = []

            args_str = self._prettify_args(args, kwargs)
            if args_str:
                log_details.append(args_str)

            self._logger.log(log_level, f"\n{log_message_header}\n" + "\n".join(log_details) if log_details else f"\n{log_message_header}")


            try:
                result = func(*args, **kwargs)
                if log_level <= logging.DEBUG and not hasattr(result, "__len__") and (not isinstance(result, str) or len(result) < 100) and not isinstance(result, (int, float, bool, type(None))):
                    log_details.append(f"Return Value:\n---\n{result!r}") # repr for clarity
                    self._logger.log(log_level,  f"\n{log_message_header}\n" + "\n".join(log_details) if log_details else f"\n{log_message_header}")
                return result
            except Exception as e:
                error_message = f"Error in '{self._name}.{name}': {e}"
                self._logger.exception(error_message)
                raise  # Re-raise exception after logging

        return log_and_call

    def _prettify_args(self, args: tuple, kwargs: Dict) -> str:
        """
        Formats function arguments and keyword arguments for logging.

        Args:
            args: Function positional arguments.
            kwargs: Function keyword arguments.

        Returns:
            Formatted string of arguments.
        """
        arg_strings = []
        for arg in args:
            if isinstance(arg, (dict, list)):
                try:
                    arg_strings.append(f"Positional Arg (JSON):\n---\n{json.dumps(arg, indent=4)}")
                except Exception:  # In case of non-serializable objects
                    arg_strings.append(f"Positional Arg (Repr):\n---\n{repr(arg)}")
            elif isinstance(arg, str) and (arg.startswith("{") or arg.startswith("[")):
                try:
                    json_like = json.loads(arg)
                    arg_strings.append(f"Positional Arg (JSON String):\n---\n{json.dumps(json_like, indent=4)}")
                except json.JSONDecodeError:
                    arg_strings.append(f"Positional Arg (String Repr):\n---\n{repr(arg)}") # if not valid json, just represent
            else:
                arg_strings.append(f"Positional Arg:\n---\n{repr(arg)}")

        arg_log_str_parts = [arg_str for arg_str in arg_strings]
        if arg_log_str_parts:
            args_log_str = "\n".join(arg_log_str_parts)
        else:
            args_log_str = None


        kwarg_strings = []
        for k, v in kwargs.items():
            kwarg_strings.append(f"Keyword Arg: {k} =\n---  {repr(v)}")

        kwargs_log_str_parts = [kwarg_str for kwarg_str in kwarg_strings]
        if kwargs_log_str_parts:
            kwargs_log_str = "\n".join(kwargs_log_str_parts)
        else:
            kwargs_log_str = None


        if args_log_str and kwargs_log_str:
            return f"Arguments:\n---\n{args_log_str}\n\n{kwargs_log_str}"
        elif args_log_str:
            return f"Arguments:\n---\n{args_log_str}"
        elif kwargs_log_str:
            return f"Arguments:\n---\n{kwargs_log_str}"
        return "" # No args or kwargs


    def __dir__(self) -> List[str]:
        """
        Returns attributes of the wrapped module for `dir()` introspection.
        """
        return dir(self._module)

    def __repr__(self) -> str:
        """
        String representation of ModWrapper instance.
        """
        return f"<{self.__class__.__name__}({self._name})>"

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Allows calling the wrapped module instance as a function (if module is callable).
        """
        return self.__getattr__("__call__")(*args, **kwargs)
