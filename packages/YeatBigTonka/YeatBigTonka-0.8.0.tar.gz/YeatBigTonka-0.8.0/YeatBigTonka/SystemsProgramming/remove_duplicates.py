def sum_decorator(func):
    """
    Простой декоратор для метода вычисления суммы.
    Например, можно добавить логирование, кэширование и т.д.
    Здесь для демонстрации просто выводим сообщение.
    """

    def wrapper(self, *args, **kwargs):
        # Дополнительная логика
        # print("Вычисляем сумму элементов массива...")
        return func(self, *args, **kwargs)

    return wrapper


class Class:
    def __init__(self, nums: list[int]):
        """
        Инициализация экземпляра.

        :param nums: Отсортированный по неубыванию массив натуральных чисел.
        """
        self.nums = nums
        self.solution = []  # результат после removeDuplicates

    def removeDuplicates(self):
        """
        Сохраняет в self.solution все уникальные элементы self.nums в порядке их появления,
        а оставшиеся позиции заполняет '_'.

        Сложность по времени: O(N), где N = len(nums).
        Сложность по памяти: O(N), чтобы хранить результат.
        """
        # Если массив пуст, просто сохраняем пустое решение
        if not self.nums:
            self.solution = []
            return

        # Сформируем список уникальных элементов
        unique = []
        unique.append(self.nums[0])

        for i in range(1, len(self.nums)):
            if self.nums[i] != self.nums[i - 1]:
                unique.append(self.nums[i])

        # Теперь нужно заполнить оставшиеся позиции символами '_'
        # чтобы длина self.solution равнялась len(self.nums)
        underscores_needed = len(self.nums) - len(unique)
        self.solution = unique + ["_"] * underscores_needed

    @sum_decorator
    def all_sum(self) -> int:
        """
        Возвращает сумму всех элементов исходного массива nums.
        """
        return sum(self.nums)

    def __str__(self):
        """
        Возвращает строку:
        "После преобразования массив [исходный] будет выглядеть так: [обработанный]"
        """
        # Преобразуем в строковый вид для наглядности
        return (f"После преобразования массив {self.nums} будет выглядеть так: "
                f"{self.solution}")


if __name__ == "__main__":
    # Пример 1
    a = Class([0, 0, 1, 1, 1, 2, 2, 3, 3, 4])
    a.removeDuplicates()
    print(
        a)  # После преобразования массив [0, 0, 1, 1, 1, 2, 2, 3, 3, 4] будет выглядеть так: [0, 1, 2, 3, 4, '_', '_', '_', '_', '_']
    print(a.all_sum())  # 17

    # Пример 2
    b = Class([0, 1, 1, 3, 3, 4, 4, 4, 4, 5])
    b.removeDuplicates()
    print(
        b)  # После преобразования массив [0, 1, 1, 3, 3, 4, 4, 4, 4, 5] будет выглядеть так: [0, 1, 3, 4, 5, '_', '_', '_', '_', '_']
    print(b.all_sum())  # 29
