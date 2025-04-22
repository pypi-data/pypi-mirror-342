# extract-numbers

![Build Status](https://github.com/talhaawan/extract-numbers/actions/workflows/build.yml/badge.svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/extract-numbers)
![PyPI Version](https://img.shields.io/pypi/v/extract-numbers)
![License](https://img.shields.io/pypi/l/extract-numbers)

> Extract numbers from strings, with support for commas, decimals, negatives, and the European format.

---

## Installation

```bash
pip install extract-numbers
```

Or if you're installing from source:

```bash
pip install -e .
```

## Usage

```py
from extract_numbers import ExtractNumbers

extractor = ExtractNumbers()

text = "100,000 results found"
extractor.extractNumbers(text)
# => ['100,000']

```

## API

### ExtractNumbers(options: dict = None)

Create a new extractor instance with optional config.

### .extractNumbers(text: str) -> List[str | int | float]

Extracts all valid numbers from the given string, based on the configured options.

## Examples

### Basic Extraction

```py
extractor = ExtractNumbers()

extractor.extractNumbers("3030 results found")
# => ['3030']

extractor.extractNumbers("50 out of 100")
# => ['50', '100']
```

### Negatives

```py
extractor.extractNumbers("Temperature: -15°C, yesterday: -22, before: -20.5")
# => ['-15', '-22', '-20.5']

extractor.extractNumbers("-170,000, -222,987 and -222,987,899.70 respectively.")
# => ['-170,000', '-222,987', '-222,987,899.70']

```

### Commas and Decimals

```py
extractor.extractNumbers("100,000 out of 220,000,000 people")
# => ['100,000', '220,000,000']

extractor.extractNumbers("Your rating is 8.7")
# => ['8.7']

extractor.extractNumbers("Your balance: $100,000.77, previous: $90,899.89")
# => ['100,000.77', '90,899.89']

```

---

## Options

Type: `Object`

### as_string

Type: `bool`
Default: `True`

If set to `False`, all numbers are returned as `int` or `float` types.

```py
ExtractNumbers({ 'as_string': False }).extractNumbers("7.7, 3030, 90,899,232.89 and -222,987,899.9")
# => [7.7, 3030, 90899232.89, -222987899.9]
```

### remove_commas

Type: `bool`
Default: `False`
Works only when `as_string=True`.

Removes thousands separators from the returned number strings.

```py
ExtractNumbers({ 'remove_commas': True }).extractNumbers("100,000,000 and -222,987,899.9")
# => ['100000000', '-222987899.9']
```

### european_format

Type: `bool`
Default: `False`
Works only when `as_string=True`.

Enables European number formatting (e.g., 1.000.000,99 instead of 1,000,000.99).

```py
ExtractNumbers({ 'european_format': True }).extractNumbers("1.000.000,77")
# => ['1.000.000,77']

ExtractNumbers({ 'european_format': True, 'as_string': False }).extractNumbers("1.000.000,77")
# => [1000000.77]
```

With `remove_commas=True`:

```py
ExtractNumbers({ 'european_format': True, 'remove_commas': True }).extractNumbers("1.000.000,77")
# => ['1000000,77']
```

> 💡 Note: The decimal comma is preserved for `as_string=True` to support formatting needs. Use `as_string=False` to convert to a float.

---

## Contributing

Contributions, issues, and feature requests are welcome!

Feel free to:

- Fork the repo
- Create a new branch
- Submit a pull request

If you're fixing a bug or adding a feature, please include a clear description in your PR.

Ensure your changes are covered by tests.

---

## Test Coverage

To run tests:

```bash
pytest
```

## License

MIT © Talha Awan
