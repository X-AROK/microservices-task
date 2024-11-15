import inspect
import logging
import sys
from functools import wraps
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
fileHandler = logging.FileHandler("logs/service.log", mode="a+")
stdoutHandler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
fileHandler.setFormatter(formatter)
stdoutHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(stdoutHandler)


def log(on_success: str, on_failure: str):
    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)

        if is_async:

            @wraps(func)
            async def wrapper(*args, **kwargs):
                result = None
                error = None
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    error = e

                if error:
                    logger.error(on_failure.format(error=str(error)))
                    raise error

                if isinstance(result, BaseModel):
                    logger.info(on_success.format(result.model_dump(mode="python")))
                elif isinstance(result, dict):
                    logger.info(on_success.format(**result))
                else:
                    logger.info(on_success.format(**result.__dict__))

                return result

            return wrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            error = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error = e

            if error:
                logger.error(on_failure.format(error=str(error)))
                raise error

            if isinstance(result, BaseModel):
                logger.info(on_success.format(**result.model_dump(mode="python")))
            elif isinstance(result, dict):
                logger.info(on_success.format(**result))
            else:
                logger.info(on_success.format(**result.__dict__))

            return result

        return wrapper

    return decorator
