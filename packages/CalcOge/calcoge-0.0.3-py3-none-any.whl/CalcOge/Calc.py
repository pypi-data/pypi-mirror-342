def convert_to(number, base):
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while number > 0:
        result = (digits[number % base] + result)
        number //= base
    return result


class CalcToNotation:
    def __init__(self, data, base=10, translation=10, printer=True, many=False):
        if not data or not isinstance(data, str) and not many:
            raise Exception(f'Incorrect input. {f'Was used {type(data)}.' if not isinstance(data, str)
                            else 'Was transferred empty object.'}')
        elif isinstance(data, str) and not many:
            data = [(data, base)]

        if not data or not isinstance(data, list) and many:
            raise Exception(f'Incorrect input. {f'Was used {type(data)}.' if not isinstance(data, list)
                            else 'Was transferred empty object.'}')

        if base < 2 or base > 36:
            raise Exception(f'Incorrect input. You entered base "{base}"')
        if translation < 2 or translation > 36:
            raise Exception(f'Incorrect input. You entered translate "{translation}"')
        self.printer = printer
        self.translate = translation
        self.many = many

        self.results = []
        for i in range(len(data)):
            if data[i][1] == 10:
                result = convert_to(int(data[i][0]), self.translate)
            elif self.translate == 10:
                result = int(data[i][0], data[i][1])
            else:
                result = convert_to(int(data[i][0], data[i][1]), self.translate)
            self.results.append(result)
            if self.printer:
                print(f'{data[i][0]} ({data[i][1]}) = {result} ({self.translate})')

    def comparison(self):
        if not self.many:
            raise Exception(f'Incorrect settings. Impossible to use "comparison" without "many"')
        print(f'Max: {convert_to(max(int(self.results[i], self.translate) for i in range(len(self.results))), self.translate)} '
              f'|| Min: {convert_to(min(int(self.results[i], self.translate) for i in range(len(self.results))), self.translate)}')
        return False


CalcToNotation([('2198129', 10), ('2198rte', 30), ('219812oiu9', 31), ('219812poiop9', 32)], translation=16, many=True).comparison()