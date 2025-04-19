class Class:
    def __init__(self, num: int):
        """
        Инициализация экземпляра.

        :param num: натуральное число (количество итераций 'Посчитай и скажи').
        """
        self.num = num  # Сколько раз выполнять операцию
        self.solution = ""  # Итоговая строка после выполнения всех итераций
        self._log = []  # Сюда сохраним пошаговые результаты для печати

    def countAndSay(self):
        """
        Выполняет операцию 'Посчитай и скажи' self.num раз,
        начиная с '1' (т.е. countAndSay(1) = '1').

        Итоговая последовательность сохраняется в self.solution.
        Подробности каждого шага сохраняются в self._log.
        """
        # Очищаем лог на случай повторного вызова
        self._log.clear()

        current = "1"
        # Шаг 1 — сразу запоминаем
        self._log.append((1, current))

        # Повторяем процесс со 2-го до num-го раз
        for i in range(2, self.num + 1):
            current = self._next_count_and_say(current)
            self._log.append((i, current))

        # Финальный результат
        self.solution = current

    def _next_count_and_say(self, s: str) -> str:
        """
        Получает строку s и «произносит» ее:
          - Считываем подряд идущие одинаковые цифры,
          - Формируем фрагмент 'количество + цифра',
          - Склеиваем фрагменты.

        Пример:
          s = "21" -> «одна 2» + «одна 1» -> "1211"
        """
        result = []
        i = 0
        while i < len(s):
            count = 1
            digit = s[i]

            # Считаем, сколько подряд идущих одинаковых символов
            while i + 1 < len(s) and s[i + 1] == digit:
                i += 1
                count += 1

            # Добавляем "count" и "digit" в результат
            result.append(str(count))
            result.append(digit)

            i += 1

        return "".join(result)

    def __str__(self):
        """
        Печатает результат в формате:

        Выполнение операции N раз дает ответ SOLUTION
        countAndSay(1) = "..."
        countAndSay(2) = "..."
        ...
        countAndSay(N) = "..."
        """
        if not self.solution:
            # Если метод countAndSay() ещё не вызывался
            return "Операция не выполнена, решение отсутствует."

        lines = [f"Выполнение операции {self.num} раз дает ответ {self.solution}"]
        for step_num, value in self._log:
            lines.append(f'countAndSay({step_num}) = "{value}"')
        return "\n".join(lines)


# Примеры использования:
if __name__ == "__main__":
    # Пример 1:
    a = Class(4)
    a.countAndSay()
    print(a)
    """
    Ожидаемый вывод:
    Выполнение операции 4 раз дает ответ 1211
    countAndSay(1) = "1"
    countAndSay(2) = "11"
    countAndSay(3) = "21"
    countAndSay(4) = "1211"
    """

    # Пример 2:
    b = Class(7)
    b.countAndSay()
    print(b)
    """
    Ожидаемый вывод (последняя строка – 7-я итерация):
    Выполнение операции 7 раз дает ответ 13112221
    ...
    countAndSay(7) = "13112221"
    """
