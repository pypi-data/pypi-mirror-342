# pylatinize: Lightweight Python Unicode Transliteration Library

[![PyPI Version](https://img.shields.io/pypi/v/pylatinize.svg)](https://pypi.org/project/pylatinize/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pylatinize.svg)](https://pypi.org/project/pylatinize/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A **lightweight** and **open-source Python package** providing robust Unicode transliteration to **Latin ASCII**. This library allows conversion of Unicode characters and sequences to their Latin ASCII equivalents or approximations using configurable mappings and Unicode normalization forms.

## Installation

### PyPi

```bash
pip install pylatinize
```

## Usage

The core functionality is provided by the `PyLatinize` class. You initialize it with one or more mapping dictionaries (including an optional `custom_mapping`) and then use the `decompose` method to convert text.

```python
from pylatinize import PyLatinize, Normalization, default_mapping, emoji_mapping

# Define your mapping(s) - these map unicode sequences/characters to ASCII
# These would typically be defined in your mappings.py file
my_base_mappings = (
    default_mapping, # Use the imported default mapping
    emoji_mapping,   # Use the imported emoji mapping
)

# Define a custom mapping to use during initialization
my_custom_init_map = {
    "©": "(c)",
    "€": "Euro", # Override the default Euro mapping if needed
    "✨": "(sparkle)"
}


# Create an instance of PyLatinize with base mappings and a custom mapping
latinizer_with_custom = PyLatinize(my_base_mappings, custom_mapping=my_custom_init_map)

# Decompose a string using the combined mappings
unicode_text = "Ahoj, toto je česká věta s € symbolom a veselým smajlíkom 😊 a autorskými právami © a trochou ✨."
ascii_text = latinizer_with_custom.decompose(unicode_text)

print(f"Original: {unicode_text}")
print(f"Decomposed: {ascii_text}")
# Original: Ahoj, toto je česká věta s € symbolom a veselým smajlíkom 😊 a autorskými právami © a trochou ✨.
# Decomposed: Ahoj, toto je ceska veta s Euro symbolom a veselym smajlikom smiling face with smiling eyes a autorskymi pravami (c) a trochou (sparkle).


# Create an instance with only default and emoji mappings
latinizer_default = PyLatinize((default_mapping, emoji_mapping))

# Decompose a German sentence with different normalization forms
german_text = "Fünfzehn Gänse saßen auf der Wiese."
ascii_text = latinizer_default.decompose(german_text)

print(f"Original: {german_text}")
print(f"Decomposed: {ascii_text}")
# Original: Fünfzehn Gänse saßen auf der Wiese.
# Decomposed: Fuenfzehn Gaense sassen auf der Wiese.

vietnamese_text = "Xin chào thế giới! Đây là một câu tiếng Việt."
ascii_text_nomap = latinizer_default.decompose(vietnamese_text)

print(f"Original: {vietnamese_text}")
print(f"Decomposed (No Mapping): {ascii_text_nomap}")
# Original: Xin chào thế giới! Đây là một câu tiếng Việt.
# Decomposed (No Mapping): Xin chao the gioi! Day la mot cau tieng Viet.
```

## API

### `class PyLatinize`

A class for transliterating and normalizing Unicode characters and sequences to ASCII using configurable mappings and a longest-match strategy.

```python
__init__(self, mappings: tuple[Dict[str, str], ...], custom_mapping: Optional[Dict[str, str]] = None)
```

Initializes `PyLatinize` with mapping dictionaries. The dictionaries are merged, with dictionaries appearing later in the `mappings` tuple, and the `custom_mapping`, overriding earlier ones in case of key conflicts. The longest matching key in the final merged mapping is used during transliteration.

**Parameters:**

`mappings` (`tuple[Dict[str, str], ...]`): A tuple of dictionaries. Each dictionary contains Unicode character sequences (str) as keys and their desired ASCII equivalents (str) as values. Must contain at least one dictionary.
`custom_mapping` (`Optional[Dict[str, str]]`, optional): Optional custom mapping dictionary (character/sequence keys) to be merged with the provided mappings during initialization. Keys in `custom_mapping` will override keys in the `mappings` if they exist in both. Defaults to `None`.

**Raises:**

* `ValueError`:
    * If `mappings` is not a tuple.
    * If `mappings` is empty.
    * If any element within the `mappings` tuple is not a dictionary.
    * If `custom_mapping` is provided but is not a dictionary.
* `TypeError`:
    * If any key within any dictionary in the `mappings` tuple is not a string.
    * If any key within the `custom_mapping` dictionary (if provided) is not a string.

### Decompose

```python
decompose(self, text: str, normalization: Normalization = Normalization.DECOMPOSE) -> str
```

Transliterates the input `text` using the mappings configured during the `PyLatinize` instance's initialization. Applies the specified Unicode `normalization` form after transliteration. Uses a longest-match strategy for mapping lookups. Non-ASCII characters without a mapping are removed by default. Combining diacritical marks are removed after decomposition normalization (NFD or NFKD).

This method is cached using `@lru_cache` for performance on repeated identical inputs with the same normalization form.

**Parameters:**

* `text` (`str`): The text to transliterate.
* `normalization` (`Normalization`, optional): The Unicode normalization form to apply after transliteration. Must be a member of the Normalization enum. Defaults to `Normalization.DECOMPOSE` (NFD).

**Returns:**

* `str`: The transliterated ASCII text.

**Raises:**

* `ValueError`: If the `normalization` value provided is not a valid member of the `Normalization` enum.

* ValueError:
    * If the `normalization` value provided is not a valid member of the `Normalization` enum.
    * If the input `text` contains invalid Unicode characters (e.g., unpaired surrogates).
* TypeError: If `text` is not a string.

### `Normalization` (enum)

```python
enum Normalization
```

An enumeration representing standard Unicode normalization forms as defined in the Unicode Standard Annex #15.

**Members:**

`DECOMPOSE` (`"NFD"`): Normalization Form Canonical Decomposition. Characters are decomposed into their base characters and combining marks.
`COMPOSE` (`"NFC"`): Normalization Form Canonical Composition. Characters are composed into their shortest possible representation using precomposed forms where available.
`COMPATIBILITY_COMPOSE` (`"NFKC"`): Normalization Form Compatibility Composition. Similar to NFC but also includes compatibility decompositions and compositions (e.g., ligatures are decomposed).
`COMPATIBILITY_DECOMPOSE` (`"NFKD"`): Normalization Form Compatibility Decomposition. Similar to NFD but also includes compatibility decompositions (e.g., ligatures are decomposed).

### Mapping Dictionaries

The `pylatinize` library exposes predefined mapping dictionaries that you can use or extend when initializing the `PyLatinize` class. These dictionaries define how specific Unicode characters or sequences are converted to their ASCII equivalents.

**`default_mapping`**

```python
default_mapping: Dict[str, str]
```

This dictionary is intended to hold a baseline set of transliteration mappings for common non-ASCII characters (e.g., accented letters, special symbols, currency symbols).

**`emoji_mapping`**

```python
emoji_mapping: Dict[str, str]
```

This dictionary is specifically designed to hold transliteration mappings for converting Unicode emojis into text-based ASCII representations (e.g., 🏴󠁧󠁢󠁷󠁬󠁳󠁿 flag: Wales, 🏃‍♂️‍➡️ man running facing right).

## License

`pylatinize` is licensed under the terms of the BSD 3-Clause License.