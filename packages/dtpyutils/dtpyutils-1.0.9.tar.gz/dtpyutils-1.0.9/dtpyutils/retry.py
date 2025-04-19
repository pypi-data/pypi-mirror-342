import asyncio
import inspect
import logging
import time
from functools import wraps
from .exception import exception_to_dict
from .jsonable_encoder import jsonable_encoder


async def retry_async(func, *args, sleep_time=2, max_attempts=3, backoff=2, exceptions=(Exception,), log_tries: bool = False, **kwargs):
    delay = sleep_time
    for attempt in range(1, max_attempts + 1):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            error_dict = exception_to_dict(e)
            error_dict['kwargs'] = jsonable_encoder(kwargs)
            error_dict['args'] = jsonable_encoder(args)
            if attempt == max_attempts:
                logging.error(
                    msg=f"We could not finish the current job in the function {func.__name__}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Error at {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
                raise e
            elif log_tries:
                logging.warning(
                    msg=f"An error happened while we retry to run {func.__name__} at the {attempt} attempt{'s' if attempt > 1 else ''}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Warning at retrying {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
            await asyncio.sleep(delay)
            delay *= backoff


def retry(func, *args, sleep_time=2, max_attempts=3, backoff=2, exceptions=(Exception,), log_tries: bool = False, **kwargs):
    if inspect.iscoroutinefunction(func):
        return retry_async(
            func,
            *args,
            sleep_time=sleep_time,
            max_attempts=max_attempts,
            backoff=backoff,
            exceptions=exceptions,
            **kwargs
        )

    delay = sleep_time
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            error_dict = exception_to_dict(e)
            error_dict['kwargs'] = jsonable_encoder(kwargs)
            error_dict['args'] = jsonable_encoder(args)
            if attempt == max_attempts:
                logging.error(
                    msg=f"We could not finish the current job in the function {func.__name__}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Error at {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
                raise e
            elif log_tries:
                logging.warning(
                    msg=f"An error happened while we retry to run {func.__name__} at the {attempt} attempt{'s' if attempt > 1 else ''}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Warning at retrying {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
            time.sleep(delay)
            delay *= backoff


def retry_wrapper(max_attempts=3, sleep_time=2, backoff=2, exceptions=(Exception,), log_tries: bool = False):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await retry_async(
                func,
                *args,
                max_attempts=max_attempts,
                sleep_time=sleep_time,
                backoff=backoff,
                exceptions=exceptions,
                log_tries=log_tries,
                **kwargs
            )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return retry(
                func,
                *args,
                max_attempts=max_attempts,
                sleep_time=sleep_time,
                backoff=backoff,
                exceptions=exceptions,
                log_tries=log_tries,
                **kwargs
            )

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
