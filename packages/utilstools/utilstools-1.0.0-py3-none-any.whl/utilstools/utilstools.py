# import utilstools
class Counter:
    @staticmethod
    def count(from_, to, step=1):
        if step == 0:
            print('Err :: step == 0')
            return
        count = 0
        if step > 0:
            for i in range(from_, to + 1, step):
                print(i)
                count += 1
        else:
            for i in range(from_, to - 1, step):
                print(i)
                count += 1
    @staticmethod
    def count_vowels(string):
        vowels = "aeiouAEIOU"
        count = sum(1 for char in string if char in vowels)
        print(count)
    @staticmethod
    def count_words(string):
        print(len(string.split()))
class StringManip:
    @staticmethod
    def reversed_string(string):
        print(string[::-1])
    @staticmethod
    def remove_spaces(string):
        print(string.replace(" ", ""))
    @staticmethod
    def remove_spec_char(string):
        print(''.join(filter(str.isalnum, string)))
    @staticmethod
    def remove_int(string):
        print(''.join(filter(lambda c: not c.isdigit(), string)))
    @staticmethod
    def find_double(items):
        doubles = {item for item in items if items.count(item) > 1}
        print(list(doubles))
    @staticmethod
    def capitalize(string):
        print(string.capitalize())
    @staticmethod
    def includes_substring(string, substring):
        print(substring in string)
    @staticmethod
    def count_occurrences(string, char):
        print(string.count(char))
class MathUtils:
    @staticmethod
    def sqr(nbr):
        print(nbr ** 2)
    @staticmethod
    def mult_table(nbr):
        print([nbr * i for i in range(1, 11)])
    @staticmethod
    def factorial(n):
        def fact(n):
            return 1 if n <= 1 else n * fact(n - 1)
        print(fact(n))
    @staticmethod
    def is_prime(n):
        if n <= 1:
            print(False)
        else:
            print(all(n % i != 0 for i in range(2, n)))
    pi = 3.141592653589793
class DateUtils:
    @staticmethod
    def now_date():
        from datetime import datetime
        print(datetime.now().strftime('%Y-%m-%d'))
    @staticmethod
    def now_time():
        from datetime import datetime
        print(datetime.now().strftime('%H:%M:%S'))
    @staticmethod
    def format_date(date, format_='date'):
        from datetime import datetime
        dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if format_ == 'date':
            print(dt.strftime('%Y-%m-%d'))
        elif format_ == 'time':
            print(dt.strftime('%H:%M:%S'))
        else:
            print(dt.strftime('%Y-%m-%d %H:%M:%S'))
class ArrayUtils:
    @staticmethod
    def sort_array(arr):
        print(sorted(arr))
    @staticmethod
    def filter_even(arr):
        print([num for num in arr if num % 2 == 0])
    @staticmethod
    def sum_array(arr):
        print(sum(arr))
class Validator:
    @staticmethod
    def is_email(string):
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        print(bool(re.match(email_regex, string)))
    @staticmethod
    def is_phone_number(string):
        import re
        phone_regex = r'^\+?\d{10,15}$'
        print(bool(re.match(phone_regex, string)))
    @staticmethod
    def is_empty(string):
        print(not string.strip())
class Logger:
    @staticmethod
    def log(message):
        from datetime import datetime
        print(f"[LOG] {datetime.now().isoformat()} - {message}")
    @staticmethod
    def error(message):
        from datetime import datetime
        print(f"[ERROR] {datetime.now().isoformat()} - {message}")
class mannage:
    @staticmethod
    def info():
        return {
            "version": "0.1.0",
            "author": "Nickels",
            "mail": "Nickels74130@outlook.fr",
        }
    @staticmethod
    def all_info():
        print("version\t:\t0.1.0")
        print("author\t:\tNickels")
        print("mail\t:\tNickels74130@outlook.fr")