def convert_to(number, base):
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    while number > 0:
        result = (digits[number % base] + result)
        number //= base
    return result


class Calc:
    def __init__(self, data_entry, base, translation, printer=True):
        if not data_entry or not isinstance(data_entry, str):
            raise Exception(f'Incorrect input. {f'Was used {type(data_entry)}.' if not isinstance(data_entry, str)
                            else 'Was transferred empty object.'}')
        if base < 2 or base > 36:
            raise Exception(f'Incorrect input. You entered base "{base}"')
        if translation < 2 or translation > 36:
            raise Exception(f'Incorrect input. You entered translate "{translation}"')
        self.data = data_entry
        self.printer = printer
        self.base = base
        self.translate = translation

    def calculate(self):
        if self.base == 10:
            result = convert_to(self.data, self.translate)
        elif self.translate == 10:
            result = int(self.data, self.base)
        else:
            result = convert_to(int(self.data, self.base), self.translate)
        if self.printer:
            print(f'{self.data} ({self.base}) = {result} ({self.translate})'.upper())


Calc('e214wq', 36, 26).calculate()
