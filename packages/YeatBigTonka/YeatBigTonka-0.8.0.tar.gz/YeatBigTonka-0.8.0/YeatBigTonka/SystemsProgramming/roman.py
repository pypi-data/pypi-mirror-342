def roman_cache_decorator(func):
    """
    Декоратор, который кэширует римское представление числа.
    """
    cache = {}  # общий кэш для всех экземпляров по ключу-числу

    def wrapper(self):
        if self.num in cache:
            print("Берем число из кэша...")
            result = cache[self.num]
        else:
            print("Вычисляем число...")
            result = func(self)
            cache[self.num] = result

        # Сохраняем результат в атрибут solution экземпляра
        self.solution = result
        return result

    return wrapper


class Class:
    def __init__(self, num: int):
        """
        Инициализация:
        num — натуральное число (предполагается, что num > 0).
        solution — строка, куда будем записывать римское представление числа.
        """
        self.num = num
        self.solution = ""

    @roman_cache_decorator
    def intToRoman(self) -> str:
        """
        Метод перевода числа self.num в римскую систему счисления.
        Возвращает римское представление в виде строки.

        Сложность по времени и памяти ~ O(N), где N = len(str(self.num)).
        """
        # Для упрощения будем считать, что num <= 3999 (стандартные римские цифры).
        # Если нужно поддерживать большие числа, логику нужно расширить.
        num_str = str(self.num)  # Десятичная запись числа
        n = len(num_str)

        # Римские обозначения для единиц (ones), десятков (tens), сотен (hundreds) и тысяч (thousands)
        thousands = ["", "M", "MM", "MMM"]  # Допустим, не идём выше 3000
        hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

        val = self.num
        # «Разбиваем» число на тысячи, сотни, десятки, единицы
        rom = []
        # тысячи
        rom.append(thousands[val // 1000])
        val %= 1000
        # сотни
        rom.append(hundreds[val // 100])
        val %= 100
        # десятки
        rom.append(tens[val // 10])
        val %= 10
        # единицы
        rom.append(ones[val])

        # Склеиваем результат
        return "".join(rom)

    def __str__(self):
        """
        Вывод в формате:
        Число X в римской системе счисления равно Y
        """
        return f"Число {self.num} в римской системе счисления равно {self.solution}"


if __name__ == "__main__":
    # Пример 1
    a = Class(495)
    a.intToRoman()  # Первый вызов — вычисляется и кэшируется
    print(a)  # Число 495 в римской системе счисления равно CDXCV
    a.intToRoman()  # Второй вызов — берем из кэша
    print(a)

    # Пример 2
    b = Class(1949)
    b.intToRoman()  # Вычисляется и кэшируется
    print(b)  # Число 1949 в римской системе счисления равно MCMXLIX
    b.intToRoman()  # Берем из кэша
    print(b)
