import asyncio
import contextvars
from concurrent.futures import Executor
from functools import partial
from typing import Any, Callable

BlockingFunction = Callable[..., Any]


async def blocking_func_to_async(
    executor: Executor, func: BlockingFunction, *args, **kwargs
):
    """Run a potentially blocking function within an executor.

    Args:
        executor (Executor): The concurrent.futures.Executor to run the function within.
        func (ApplyFunction): The callable function, which should be a synchronous
            function. It should accept any number and type of arguments and return an
            asynchronous coroutine.
        *args (Any): Any additional arguments to pass to the function.
        **kwargs (Any): Other arguments to pass to the function

    Returns:
        Any: The result of the function's execution.

    Raises:
        ValueError: If the provided function 'func' is an asynchronous coroutine
            function.

    This function allows you to execute a potentially blocking function within an
    executor. It expects 'func' to be a synchronous function and will raise an error
    if 'func' is an asynchronous coroutine.
    """
    if asyncio.iscoroutinefunction(func):
        raise ValueError(f"The function {func} is not blocking function")

    # This function will be called within the new thread, capturing the current context
    ctx = contextvars.copy_context()

    def run_with_context():
        return ctx.run(partial(func, *args, **kwargs))

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_with_context)
