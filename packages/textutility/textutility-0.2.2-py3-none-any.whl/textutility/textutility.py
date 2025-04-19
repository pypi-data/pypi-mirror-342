def is_str(value):
    """
    Returns True if the input is a string-like value.
    Returns False if the input looks like a number or a boolean ("True"/"False").
    """
    if value.title() in ('True', 'False'):
        return False
    elif value.lstrip('-').isdigit():
        return False
    elif value.count('.') == 1 and value.replace('.', '').lstrip('-').isdigit():
        if not value.startswith('.') and not value.endswith('.'):
            return False
    return True
def is_type(text="", _type=""):
    """
Checks if the given text matches the specified data type.

Args:
    text (str): The input string to check.
    _type (str): The expected type to check against ('int', 'float', 'bool', etc.).

Returns:
    bool: True if the text matches the given type, False otherwise.
"""
    if text.title() in ('True', 'False'):
        return _type == "bool"

    elif text.lstrip('-').isdigit():
        return _type == "int"

    elif text.count('.') == 1 and text.replace('.', '').lstrip('-').isdigit():
        if not text.startswith('.') and not text.endswith('.'):
            return _type == "float"

    return _type == "str"
def only_letters(value):
    """
    Returns True if the input contains only alphabetic characters.
    """
    return value.isalpha()

def repeat(value, times):
    """
    Returns the input string repeated `times` times.
    """
    return value * times

def reverse(text, line=True):
    """
    Returns a mirrored version of the text.

    Args:
        text (str): Input text to mirror.
        line (bool): If True, adds a "|" separator between original and mirrored version.

    Returns:
        str: Mirrored text.

    Examples:
        mirror_text("abc")       ➜ "abc|cba"
        mirror_text("abc", False) ➜ "cba"
    """
    if line: return str(text) + "|" +  str(text)[::-1]
    return str(text)[::-1]

def count_substring(value, substring):
    """
    Returns the number of times `substring` appears in `value`.
    """
    return value.count(substring)

def no_spaces(value):
    """
    Removes leading and trailing spaces, then replaces all spaces with hyphens.
    """
    return value.strip().replace(' ', '-')

def is_anagram(value1, value2):
    """
    Returns True if both input strings are anagrams of each other.
    """
    return sorted(value1) == sorted(value2)
def is_palindrome(text):
    """
    Checks if `text` is the same backwards.
    """
    return text == text[::-1]
def longest_prefix(value1, value2):
    """
    Returns the longest common prefix between two strings.
    """
    prefix = ''
    for i in range(min(len(value1), len(value2))):
        if value1[i] == value2[i]:
            prefix += value1[i]
        else:
            break
    return prefix

def reverse_bits(char):
    """
    Returns a character whose ASCII code is the bitwise negation of the input character.
    Works only with single characters (8-bit ASCII).
    """
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("Please provide a single character!")

    value = ord(char)
    flipped = ~value & 0xFF  # limit to 8-bit range
    return chr(flipped)
def string_from_int(*numbers, base=10):
    """
    Converts a sequence of numbers (as strings or integers) from a given base into a string.

    Args:
        *numbers: Values to decode into characters.
        base (int): The base in which the numbers are represented (e.g., 2, 10, 16).

    Returns:
        str: Decoded string from the given numbers.
    
    Raises:
        ValueError: If a number is invalid for the given base or the base itself is unsupported.
    """
    if base != 0 and (base < 2 or base > 36):
        raise ValueError("base must be >= 2 and <= 36, or 0")
    string = ""
    for number in numbers:
        try:
            string += chr(int(number, base))
        except ValueError:
            raise ValueError(f"{number} not in base: {base}, base ranges from 0 to {base-1}")
    return string
def to_snake_case(text):
    """
    Converts a string to snake_case without using regex.
    Handles camelCase, PascalCase, spaces and hyphens.
    """
    result = []
    for i, char in enumerate(text):
        if char.isupper():
            if i > 0 and (text[i-1].islower() or text[i-1].isdigit()):
                result.append('_')
            result.append(char.lower())
        elif char in {' ', '-'}:
            result.append('_')
        else:
            result.append(char)
    return ''.join(result)
def to_camel_case(text):
    """
    Converts a string to camelCase without using regex.
    Accepts snake_case, kebab-case and space-separated strings.
    """
    parts = []
    current = ''
    for char in text:
        if char in {'_', '-', ' '}:
            if current:
                parts.append(current)
                current = ''
        else:
            current += char
    if current:
        parts.append(current)

    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
def to_1337(text):
    """
    Converts text to the famous 1337 style.
    """
    replacements = {'a': '@', 'e': '3', 'i': '!', 'l': '1', 'o': '0', 't': '7', 's': '5', 'z': '2'}
    return ''.join(replacements.get(c.lower(), c) for c in text)
def change_data_type(text, _type="string"):
    """
    Converts a string into the specified `_type` ('int', 'float', 'bool', 'string').
    Supports minus sign. Works without using int(), float(), or eval().

    Args:
        text (str): The input string.
        _type (str): The type to convert to: 'int', 'float', 'bool', or 'string'.

    Returns:
        The converted value.

    Raises:
        ValueError: If the value contains invalid characters.
        NotImplementedError: For unknown bool strings.
        TypeError: For unsupported type names.
    """
    if _type == "int":
        digits = "0123456789"
        s = text.strip()
        negative = False

        if s.startswith("-"):
            negative = True
            s = s[1:]

        result = 0
        for char in s:
            if char not in digits:
                raise ValueError(f"Invalid character: {char}")
            result = result * 10 + digits.index(char)

        return -result if negative else result
    elif _type == "bool":
        if text == "True":
            return True
        elif text == "False":
            return False
        elif text == "None":
            return None
        else:
            raise NotImplementedError(f"There is no bool statement {text}")
    elif _type == "float":
        s = text.strip()
        negative = False

        if s.startswith("-"):
            negative = True
            s = s[1:]

        if "." not in s:
            return -change_data_type(s, "int") if negative else change_data_type(s, "int")

        integer_part, decimal_part = s.split(".")

        int_value = change_data_type(integer_part, "int") if integer_part else 0
        dec_value = change_data_type(decimal_part, "int") / (10 ** len(decimal_part))

        result = int_value + dec_value
        return -result if negative else result
    elif _type == "string":
        return text
    else:
        raise TypeError(f"There exists no data type such as {_type}")
def count_vowels(text):
    return sum(1 for c in text.lower() if c in "aeiouy")
def what_type(value=""):
    """
    Detects the basic data type of the input value as a string.

    Determines if the input string looks like a boolean, integer, float, or string.

    Args:
        value (str): The input to check. Can be a string representation of a value.

    Returns:
        str: One of 'bool', 'int', 'float', or 'string', depending on detected format.

    Examples:
        what_type("True")    ➜ "bool"
        what_type("-123")    ➜ "int"
        what_type("3.14")    ➜ "float"
        what_type("hello")   ➜ "string"
    """
    if value.title() in ('True', 'False'):
        return "bool"
    elif value.lstrip('-').isdigit():
        return "int"
    elif value.count('.') == 1 and value.replace('.', '').lstrip('-').isdigit():
        if not value.startswith('.') and not value.endswith('.'):
            return "float"
    return "string"
def exclusive_print(text):
    """
    Prints the given text inside a fancy ASCII box.

    Args:
        text (str): The message to print.
    """
    lines = text.splitlines()
    max_length = max(len(line) for line in lines)
    horizontal = "═" * (max_length + 4)

    print(f"╔{horizontal}╗")
    for line in lines:
        print(f"║  {line.ljust(max_length)}  ║")
    print(f"╚{horizontal}╝")
class printBox:
    def __init__(self, text):
        self.text = text

    def __enter__(self):
        lines = self.text.splitlines()
        max_length = max(len(line) for line in lines)
        horizontal = "═" * (max_length + 4)
        print(f"╔{horizontal}╗")
        for line in lines:
            print(f"║  {line.ljust(max_length)}  ║")
        return self  # niekoniecznie potrzebne, ale poprawnie

    def __exit__(self, exc_type, exc_val, exc_tb):
        max_length = max(len(line) for line in self.text.splitlines())
        horizontal = "═" * (max_length + 4)
        print(f"╚{horizontal}╝")
