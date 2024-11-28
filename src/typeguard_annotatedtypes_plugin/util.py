# region util
import functools

INDENT_COUNT = 0


def print_input_output(func):
    __tracebackhide__ = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global INDENT_COUNT
        __tracebackhide__ = True
        args_str = [f"{arg!r}" for arg in args]
        kwargs_str = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args = ", ".join(args_str + kwargs_str)

        indent = "  " * INDENT_COUNT
        print(
            f"{indent}\033[38;5;246m➡️  {func.__name__}({all_args})\033[0m"
        )  # Gray color

        INDENT_COUNT += 1
        try:
            result = func(*args, **kwargs)
        finally:
            INDENT_COUNT -= 1

        indent = "  " * INDENT_COUNT
        color = "67" if result is None else "75"
        if isinstance(result, functools.partial):
            result_str = f"{result.func.__name__}(..., {', '.join(f'{k}={v!r}' for k, v in result.keywords.items())})"
            print(
                f"{indent}\033[38;5;{color}m⬅️  {func.__name__} ==> {result_str}\033[0m"
            )
        else:
            print(f"{indent}\033[38;5;{color}m⬅️  {func.__name__} ==> {result!r}\033[0m")
        return result

    return wrapper


def on_exception_return_none(func):
    __tracebackhide__ = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:  # noqa: E722
            return None

    return wrapper


# endregion
