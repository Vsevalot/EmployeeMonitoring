import os
import inspect
import types
import typing


def abspath_for_script_directory(
    index: int = 0,
) -> str:
    stack = inspect.stack()
    frame = stack[index + 1] if len(stack) > index else stack[index]
    return os.path.dirname(os.path.abspath(frame.filename))


def abspath_for_module(
    module: types.ModuleType,
) -> str:
    return os.path.dirname(os.path.abspath(module.__file__))


def mkdirs(
    path: str,
) -> typing.NoReturn:
    if not os.path.exists(path):
        os.makedirs(path)
