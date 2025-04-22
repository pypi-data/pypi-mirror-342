import asyncio
from pyhunt import trace, logger


@trace
async def plus_one(param):
    result = param + 1
    return result


@trace
def multiple(param):
    result = param * 2
    return result


@trace
async def async_level2(param):
    # Call sync function which returns coroutine, then await it
    added = param + 1

    result = await plus_one(added)
    multiple_result = multiple(result)

    return multiple_result


@trace
def level1(param):
    result = asyncio.run(async_level2(param))
    return result


@trace
def main():
    # Call sync async_level1, which returns coroutine, then run it
    final_result = level1(2)
    logger.info(f"Final result: {final_result}")


if __name__ == "__main__":
    main()
