from dataclasses import dataclass
from typing import Callable, Union, overload

ComparisonFunc = Callable[[Union[float, str], Union[float, str]], bool]


def less_than(forecast: Union[float, str], value: Union[float, str]) -> bool:
    return forecast < value


def less_than_equal(forecast: Union[float, str], value: Union[float, str]) -> bool:
    return forecast <= value


def equal(forecast: Union[float, str], value: Union[float, str]) -> bool:
    if not isinstance(forecast, type(value)):
        raise TypeError(
            f"'==' not supported between instances of '{type(forecast)}' and '{type(value)}'"
        )
    return forecast == value


def greater_than_equal(forecast: Union[float, str], value: Union[float, str]) -> bool:
    return forecast >= value


def greater_than(forecast: Union[float, str], value: Union[float, str]) -> bool:
    return forecast > value


def not_equal(forecast: Union[float, str], value: Union[float, str]) -> bool:
    if not isinstance(forecast, type(value)):
        raise TypeError(
            f"'!=' not supported between instances of '{type(forecast)}' and '{type(value)}'"
        )
    return forecast != value


@dataclass
class Comparison:
    key: str
    compare_func: ComparisonFunc
    value: Union[float, str]

    def compare(self, forecast: dict[str, Union[float, str]]) -> bool:
        value = forecast[self.key]
        return self.compare_func(value, self.value)


class OperatorMap:
    """A mapping of operators to their respective functions.
    Includes the standard operators, "<", "<=", "==", ">=", ">", "!=" by
    default.

    Register additional operators with the register function.
    """

    def __init__(self) -> None:
        self._operator_map: dict[str, ComparisonFunc] = {
            "<": less_than,
            "<=": less_than_equal,
            "==": equal,
            ">=": greater_than_equal,
            ">": greater_than,
            "!=": not_equal,
        }

    def register(self, operator: str, comparison: ComparisonFunc) -> None:
        """Register a new comparison function to an operator.

        Args:
            operator (str): The operator string.
            comparison (ComparisonFunc): A comparison function.
        """
        self._operator_map[operator] = comparison

    def comparison_from_string(self, config: str) -> Comparison:
        """Converts a string to a Comparison.

        Args:
            config (str): A string in the form "{key} {operator} {value}

        Raises:
            ValueError: If the operator is not registered.

        Returns:
            Comparison: The comparison described by the string.
        """
        key, operator, value = config.split(" ")
        if operator not in self._operator_map:
            raise ValueError(f"invalid comparison: {operator}")
        comparison = self._operator_map[operator]

        try:
            # set value to a float if possible
            return Comparison(key, comparison, float(value))
        except ValueError:
            # otherwise leave it as a string
            return Comparison(key, comparison, value)


# This is an instantiated OperatorMap for easy use.
operator_map = OperatorMap()
