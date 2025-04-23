#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pylatinize - A Python module for transliterating and normalizing Unicode to Latin ASCII.

This module provides functionality to convert Unicode characters and sequences
to their Latin ASCII equivalents or approximations using configurable mappings
and Unicode normalization forms.
"""
import unicodedata
import re
import enum
from typing import Dict, List, Optional, Tuple
from functools import lru_cache


class Normalization(enum.Enum):
    """
    Enum representing Unicode normalization forms.

    Members:
        DECOMPOSE: Normalization Form Canonical Decomposition (NFD).
        COMPOSE: Normalization Form Canonical Composition (NFC).
        COMPATIBILITY_COMPOSE: Normalization Form Compatibility Composition (NFKC).
        COMPATIBILITY_DECOMPOSE: Normalization Form Compatibility Decomposition (NFKD).
    """

    DECOMPOSE = "NFD"
    COMPOSE = "NFC"
    COMPATIBILITY_COMPOSE = "NFKC"
    COMPATIBILITY_DECOMPOSE = "NFKD"


class PyLatinize:
    """
    A class for transliterating and normalizing Unicode characters to ASCII
    using configurable mappings and a longest-match strategy.
    """

    def __init__(
        self,
        mappings: tuple[Dict[str, str], ...],
        custom_mapping: Optional[Dict[str, str]] = None,
    ):
        """
        Initializes PyLatinize with mapping dictionaries.

        The mappings are used to transliterate specific Unicode character
        sequences to their desired ASCII representations. The longest matching
        key in the combined mapping will be used for transliteration.

        Args:
            mappings: A tuple of dictionaries. Each dictionary contains
                      Unicode character sequences (str) as keys and their
                      desired ASCII equivalents (str) as values.
            custom_mapping: Optional custom mapping dictionary (character/sequence
                            keys) to be merged with the provided mappings during
                            initialization. Keys in `custom_mapping` will override
                            keys in the `mappings` if they exist in both.

        Raises:
            ValueError:
                - If `mappings` is not a tuple.
                - If `mappings` is empty.
                - If any element within the `mappings` tuple is not a dictionary.
                - If `custom_mapping` is provided but is not a dictionary.
            TypeError:
                - If any key within any dictionary in the `mappings` tuple is not a string.
                - If any key within the `custom_mapping` dictionary (if provided) is not a string.
        """
        if not isinstance(mappings, tuple):
            raise ValueError("Mappings must be provided as a tuple of dictionaries.")

        if not mappings:
            raise ValueError(
                "No mappings provided. Please provide at least one mapping dictionary within the tuple."
            )

        self.flat_mapping: Dict[str, str] = {}

        # Merge initial mappings using the helper method
        for i, mapping_dict in enumerate(mappings):
            if not isinstance(mapping_dict, dict):
                raise ValueError(
                    f"Mappings tuple must contain only dictionaries, found {type(mapping_dict).__name__} at index {i}."
                )
            # _merge_mapping_dict checks key types and raises TypeError
            self._merge_mapping_dict(mapping_dict)

        # Merge custom mapping if provided using the helper method
        if custom_mapping:
            if not isinstance(custom_mapping, dict):
                raise ValueError("Custom mapping must be a dictionary.")
            # _merge_mapping_dict checks key types and raises TypeError
            self._merge_mapping_dict(custom_mapping)

        self._sorted_keys = sorted(self.flat_mapping.keys(), key=len, reverse=True)

    def _merge_mapping_dict(self, mapping_dict: Dict[str, str]):
        """
        Internal helper to merge a single mapping dictionary into flat_mapping.

        Performs type checking for keys before updating the flat mapping.

        Args:
            mapping_dict: The dictionary to merge.

        Raises:
            TypeError: If any key within the `mapping_dict` is not a string.
        """
        for key in mapping_dict:
            if not isinstance(key, str):
                raise TypeError(
                    f"Mapping dictionary key must be a string, but found type {type(key).__name__}: {key}"
                )
        self.flat_mapping.update(mapping_dict)

    @property
    def flat_mapping(self) -> Dict[str, str]:
        """
        Gets the flattened dictionary of all combined mappings.

        This property provides access to the single dictionary created by
        merging all dictionaries provided during initialization, including
        any custom mapping.

        Returns:
            A dictionary containing the combined transliteration mappings.
        """
        return self._flat_mapping

    @flat_mapping.setter
    def flat_mapping(self, value: Dict[str, str]):
        """
        Sets the flattened dictionary of all combined mappings.

        This setter is primarily for internal use during initialization
        to store the combined mappings.

        Args:
            value: The dictionary to set as the flat mapping.
        """
        self._flat_mapping = value

    @property
    def _sorted_keys(self) -> List[str]:
        """
        Gets the list of mapping keys sorted by length in descending order.

        This internal property is used to efficiently perform the longest-match
        lookup during the transliteration process.

        Returns:
            A list of mapping keys sorted from longest to shortest.
        """
        return self.__sorted_keys

    @_sorted_keys.setter
    def _sorted_keys(self, value: List[str]):
        """
        Sets the list of mapping keys sorted by length in descending order.

        This setter is primarily for internal use during initialization
        to store the sorted keys.

        Args:
            value: The list of sorted mapping keys.
        """
        self.__sorted_keys = value

    @lru_cache(maxsize=1024)
    def decompose(
        self,
        text: str,
        normalization: Normalization = Normalization.DECOMPOSE,
    ) -> str:
        """
        Transliterate Unicode text using the instance's configured mappings and a longest-match strategy.

        The method iterates through the input text and attempts to match the longest
        possible sequence from the instance's mapping keys starting at the current position.
        If a match is found, the corresponding value from the mapping is appended
        to the result, and the position in the text is advanced by the length of
         the matched key. If no match is found for the character at the current
        position, the character is appended to the result if it's an ASCII
        character (<= 127); otherwise, the original character is preserved.
        Finally, the result is subjected to the specified Unicode normalization
        form, and combining diacritical marks are removed if the normalization
        form is decomposing.

        Args:
            text: The text to transliterate.
            normalization: The Unicode normalization form to apply after
                           transliteration. Defaults to Normalization.DECOMPOSE (NFD).
                           Must be a member of the Normalization enum.

        Returns:
            The transliterated ASCII text, with unmapped non-ASCII characters preserved.

        Raises:
            ValueError:
                - If the `normalization` value provided is not a valid
                  member of the `Normalization` enum.
                - If the input `text` contains invalid Unicode characters (e.g., unpaired surrogates).
            TypeError: If `text` is not a string.
        """
        if not isinstance(text, str) or not text:
            raise ValueError(
                "Text must be a non-empty string. Please provide valid text to transliterate."
            )

        try:
            text.encode("utf-8", errors="strict")
        except UnicodeEncodeError:
            raise ValueError("Input text contains invalid Unicode characters.")

        if not isinstance(normalization, Normalization):
            raise ValueError(
                f"Invalid normalization value: {normalization}. "
                f"Must be a member of the Normalization enum (e.g., Normalization.DECOMPOSE)."
            )

        # Use the instance's mapping and sorted keys directly
        current_mapping = self.flat_mapping
        sorted_keys_for_lookup = self._sorted_keys

        result = []
        i = 0
        n = len(text)

        while i < n:
            matched_key = None
            matched_value = None
            for key in sorted_keys_for_lookup:
                if text[i:].startswith(key):
                    matched_key = key
                    matched_value = current_mapping[key]
                    break
            if matched_key:
                result.append(matched_value)
                i += len(matched_key)
            else:
                char = text[i]
                # Keep ASCII characters and preserve unmapped non-ASCII characters
                result.append(char)
                i += 1

        joined_result = "".join(result)
        normalized_result = unicodedata.normalize(normalization.value, joined_result)

        # Remove combining diacritical marks after normalization if it's a decomposing form
        if normalization in (
            Normalization.DECOMPOSE,
            Normalization.COMPATIBILITY_DECOMPOSE,
        ):
            normalized_result = re.sub(r"[\u0300-\u036f]", "", normalized_result)

        return normalized_result
