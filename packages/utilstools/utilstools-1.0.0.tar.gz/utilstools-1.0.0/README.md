# utilstools

# Description

This import add sode usefull tool like : format_date, is_email, array management, validation and other

## 📦 Installation 📦

Just one command

```pip
pip install utilstools
```

## Import

```python
import utilstools
```

---

## Features and Usage

### Counter
Methods for counting operations:
- **`count(from_, to, step=1)`**: Counts numbers from `from_` to `to` using a specified step.
- **`count_vowels(string)`**: Counts the number of vowels in a string.
- **`count_words(string)`**: Counts the number of words in a string.

### StringManip
Powerful string manipulation methods:
- **`reversed_string(string)`**: Returns the reversed version of the string.
- **`remove_spaces(string)`**: Removes all spaces from the string.
- **`remove_spec_char(string)`**: Removes special characters.
- **`remove_int(string)`**: Removes digits from the string.
- **`find_double(items)`**: Finds and lists duplicate items in an array.
- **`capitalize(string)`**: Capitalizes the first letter of a string.
- **`includes_substring(string, substring)`**: Checks if the string contains the substring.
- **`count_occurrences(string, char)`**: Counts the occurrences of a character in a string.

### MathUtils
Advanced mathematical operations:
- **`sqr(nbr)`**: Calculates the square of a number.
- **`mult_table(nbr)`**: Displays the multiplication table for a number.
- **`factorial(n)`**: Computes the factorial of a number.
- **`is_prime(n)`**: Determines if a number is prime.
- **`pi`**: A constant representing the value of Pi.

### DateUtils
Methods for date and time handling:
- **`now_date()`**: Prints the current date.
- **`now_time()`**: Prints the current time.
- **`format_date(date, format_='date')`**: Formats a date string (`date`) in either date or time format.

### ArrayUtils
Array-related utilities:
- **`sort_array(arr)`**: Sorts the array in ascending order.
- **`filter_even(arr)`**: Filters even numbers from the array.
- **`sum_array(arr)`**: Computes the sum of all elements in the array.

### Validator
Validation methods:
- **`is_email(string)`**: Checks if a string is a valid email.
- **`is_phone_number(string)`**: Checks if a string is a valid phone number.
- **`is_empty(string)`**: Checks if a string is empty or consists only of whitespace.

### Logger
Tools for logging messages:
- **`log(message)`**: Logs a message with a timestamp.
- **`error(message)`**: Logs an error message with a timestamp.

### Manage
Provides metadata about the module:
- **`info()`**: Returns metadata about the module, including version, author, and email.
- **`all_info()`**: Prints all metadata information in a formatted manner.

---

## Example Usage

Here is an example demonstrating the usage of the `utilstools` module:

```python
import utilstools


# Using Counter
print("=== Counter ===")
utilstools.Counter.count(1, 10, 2)
print("Counting vowels in a string:")
utilstools.Counter.count_vowels("Hello everyone")
print("Counting words in a string:")


utilstools.Counter.count_words("This is a sentence with multiple words")
# Using StringManip
print("\n=== StringManip ===")
print("Reversing the string 'Hello':")
utilstools.StringManip.reversed_string("Hello")
print("Removing spaces:")
utilstools.StringManip.remove_spaces("This is a test")
print("Removing special characters:")
utilstools.StringManip.remove_spec_char("Hello @World#2025!")
print("Removing digits:")
utilstools.StringManip.remove_int("Today is 2025")
print("Finding duplicates in an array:")
utilstools.StringManip.find_double([1, 2, 3, 2, 4, 5, 3])
print("Capitalizing the string 'hello':")
utilstools.StringManip.capitalize("hello")
print("Checking if the string includes a substring:")
utilstools.StringManip.includes_substring("Hello world", "world")
print("Counting occurrences of 'a' in 'Abracadabra':")
utilstools.StringManip.count_occurrences("Abracadabra", 'a')
# Using MathUtils
print("\n=== MathUtils ===")
print("Square of 4:")
utilstools.MathUtils.sqr(4)
print("Multiplication table for 3:")
utilstools.MathUtils.mult_table(3)
print("Factorial of 5:")
utilstools.MathUtils.factorial(5)
print("Is 11 a prime number:")
utilstools.MathUtils.is_prime(11)
print(f"Value of pi: {utilstools.MathUtils.pi}")
# Using DateUtils
print("\n=== DateUtils ===")
print("Current date:")
utilstools.DateUtils.now_date()
print("Current time:")
utilstools.DateUtils.now_time()
print("Formatted date:")
utilstools.DateUtils.format_date("2025-04-22 18:17:00", format_="date")
print("Formatted time:")
utilstools.DateUtils.format_date("2025-04-22 18:17:00", format_="time")
# Using ArrayUtils
print("\n=== ArrayUtils ===")
print("Sorting an array:")
utilstools.ArrayUtils.sort_array([5, 3, 8, 1])
print("Filtering even numbers:")
utilstools.ArrayUtils.filter_even([1, 2, 3, 4, 5, 6])
print("Summing an array:")
utilstools.ArrayUtils.sum_array([1, 2, 3, 4, 5])
# Using Validator
print("\n=== Validator ===")
print("Checking if the string is an email:")
utilstools.Validator.is_email("test@example.com")
print("Checking if the string is a phone number:")
utilstools.Validator.is_phone_number("+1234567890")
print("Checking if the string is empty:")
utilstools.Validator.is_empty("   ")
# Using Logger
print("\n=== Logger ===")
utilstools.Logger.log("This is a log message")
utilstools.Logger.error("This is an error message")
# Using mannage
print("\n=== mannage ===")
info = utilstools.mannage.info()
print(f"Version: {info['version']}, Author: {info['author']}, Email: {info['mail']}")
print("Displaying all information:")
utilstools.mannage.all_info()
```