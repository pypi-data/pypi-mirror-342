from pyhunt import trace, logger


@trace
def sample_function(param1, param2):
    logger.info(f"Starting sample_function with params: {param1}, {param2}")
    result = param1 + param2

    return result


if __name__ == "__main__":
    result = sample_function(5, 10)
