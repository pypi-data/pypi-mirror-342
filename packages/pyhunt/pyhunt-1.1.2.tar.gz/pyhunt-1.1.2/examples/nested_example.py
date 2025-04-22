from pyhunt import trace, logger


@trace
def multiply(a, b):
    return a * b


@trace
def calculate(numbers, loop_count):
    total = 0
    # For each number, multiply by 2 in a loop of loop_count times
    for num in numbers:
        for _ in range(loop_count):
            total += multiply(num, 2)
    return total


@trace
def process_data(data, loop_count):
    processed = [x + 1 for x in data]
    result = calculate(processed, loop_count)
    return result


@trace
def main():
    data = [1, 2, 3]
    loop_count = 10

    final_result = process_data(data, loop_count)
    return final_result


if __name__ == "__main__":
    output = main()
    logger.info(f"Final output: {output}")
