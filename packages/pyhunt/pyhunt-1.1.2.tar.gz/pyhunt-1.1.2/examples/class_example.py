from pyhunt import trace, logger


@trace
class Calculator:
    def add(self, a, b):
        logger.info(f"Adding {a} + {b}")
        return a + b

    def multiply(self, a, b):
        logger.info(f"Multiplying {a} * {b}")
        return a * b


@trace
def main():
    calc = Calculator()
    sum_result = calc.add(3, 4)
    product_result = calc.multiply(3, 4)

    logger.info(f"Sum result: {sum_result}")
    logger.info(f"Product result: {product_result}")


if __name__ == "__main__":
    main()
