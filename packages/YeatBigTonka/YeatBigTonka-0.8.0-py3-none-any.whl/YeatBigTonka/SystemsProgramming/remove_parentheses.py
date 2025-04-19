def remove_parentheses(text: str) -> str:
    """
    Удаляет из строки text все подстроки, заключённые в круглые скобки, включая вложенные.
    Возвращает "очищенный" текст без скобок.
    """
    result = []
    parenthesis_count = 0

    for char in text:
        if char == '(':
            parenthesis_count += 1
        elif char == ')':
            # Закрываем одну скобку, если она была открыта
            if parenthesis_count > 0:
                parenthesis_count -= 1
        else:
            # Добавляем символ только если мы не находимся внутри скобок
            if parenthesis_count == 0:
                result.append(char)

    return "".join(result)


# Пример использования:
if __name__ == "__main__":
    text = "Это пример (ненужного текста (с вложенными скобками)) и так далее."
    cleaned = remove_parentheses(text)
    print("Исходный текст:", text)
    print("Очищенный текст:", cleaned)
