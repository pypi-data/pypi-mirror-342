from typing import List, Dict, Union
from pyhunt import trace, logger


@trace
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b


@trace
def concat_strings(s1: str, s2: str, sep: str = " ") -> str:
    return f"{s1}{sep}{s2}"


@trace
def repeat_string(s: str, times: int) -> str:
    return s * times


@trace
def combine_data(num: int, text: str, flag: bool) -> str:
    if flag:
        return f"{text} repeated {num} times: " + (text * num)
    else:
        return f"Number: {num}, Text: {text}"


@trace
def sum_list(numbers: List[int]) -> int:
    return sum(numbers)


@trace
def get_dict_keys(d: Dict[str, int]) -> List[str]:
    return list(d.keys())


@trace
def merge_dicts(d1: Dict[str, int], d2: Dict[str, int]) -> Dict[str, int]:
    merged = d1.copy()
    merged.update(d2)
    return merged


@trace
def main() -> None:
    # Test add with integers
    result1 = add(5, 7)
    # Test add with floats
    result2 = add(3.5, 2.1)
    # Test concat_strings with default separator
    result3 = concat_strings("Hello", "World")
    # Test concat_strings with custom separator
    result4 = concat_strings("Hello", "World", sep=", ")
    # Test repeat_string
    result5 = repeat_string("abc", 3)
    # Test combine_data with flag True
    result6 = combine_data(4, "test", True)
    # Test combine_data with flag False
    result7 = combine_data(10, "example", False)
    # Test sum_list with a list of numbers
    result8 = sum_list([1, 2, 3, 4, 5])
    # Test get_dict_keys with a dictionary
    result9 = get_dict_keys({"a": 1, "b": 2, "c": 3})
    # Test merge_dicts with two dictionaries
    result10 = merge_dicts({"x": 1, "y": 2}, {"y": 3, "z": 4})

    logger.info("Results:")
    logger.info(f"add(5, 7) = {result1}")
    logger.info(f"add(3.5, 2.1) = {result2}")
    logger.info(f'concat_strings("Hello", "World") = {result3}')
    logger.info(f'concat_strings("Hello", "World", sep=", ") = {result4}')
    logger.info(f'repeat_string("abc", 3) = {result5}')
    logger.info(f'combine_data(4, "test", True) = {result6}')
    logger.info(f'combine_data(10, "example", False) = {result7}')
    logger.info(f"sum_list([1, 2, 3, 4, 5]) = {result8}")
    logger.info(f'get_dict_keys({{"a": 1, "b": 2, "c": 3}}) = {result9}')
    logger.info(f'merge_dicts({{"x": 1, "y": 2}}, {{"y": 3, "z": 4}}) = {result10}')


if __name__ == "__main__":
    main()
