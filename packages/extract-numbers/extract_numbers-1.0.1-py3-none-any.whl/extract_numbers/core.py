from typing import Optional, TypedDict, List, Union
import re

class Options(TypedDict, total=False):
    as_string: bool
    remove_commas: bool
    european_format: bool

Number = Union[str, int, float]

EU_REGEX = r'-?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d+)?'
US_REGEX = r'-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'

class ExtractNumbers:
    """
    Extracts numbers from a string, supporting US and European formats.

    Options:
        - as_string (bool): Return numbers as strings. Default is True.
        - remove_commas (bool): Remove thousands separators. Works only with as_string=True.
        - european_format (bool): Interpret numbers using European style (e.g., 1.000,55). Default is False.
    """
    def __init__(self, options: Optional[Options] = None) -> None:
        self.options: Options = {
            "as_string": True,
            "remove_commas": False,
            "european_format": False
        }
        
        if isinstance(options, dict):
            for key, value in options.items():
                if key not in self.options:
                    raise ValueError(f"Invalid option '{key}'. Expected one of {list(self.options.keys())}.")
                if not isinstance(value, bool):
                    raise TypeError(f"Option '{key}' must be a boolean.")
            self.options.update(options)

    def _sanitize_number(self, number: str) -> Number:
        if self.options["european_format"]:
            number = number.replace(".", "").replace(",", ".")
        else:
            number = number.replace(",", "")
        return float(number) if "." in number else int(number)

    def extractNumbers(self, text: str) -> List[Number]:
        """
        Extracts numbers from the input text string based on configured options.

        Args:
            text (str): The text to search for numbers.

        Returns:
            List[Union[str, int, float]]: A list of numbers found in the text.
        """
        if not isinstance(text, str):
            raise ValueError(f"Invalid argument: Expected 'text' to be of type str, but got {type(text).__name__}.")

        as_string = self.options.get("as_string", False)
        remove_commas = self.options.get("remove_commas", False)
        numbers = re.findall(US_REGEX, text)
        comma_type = ","        

        if self.options.get("european_format"):             
            numbers = re.findall(EU_REGEX, text)
            comma_type = "."                                                    

        if as_string and remove_commas:            
            return [number.replace(comma_type, "") for number in numbers]
        
        if not as_string:
          return [self._sanitize_number(n) for n in numbers]
        
        return numbers
