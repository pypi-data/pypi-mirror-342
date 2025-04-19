def insert_into_heap(heap, new_element):
    """
    Вставляет новый элемент в бинарную кучу (min-heap) и восстанавливает свойство кучи.

    :param heap: list, текущая бинарная куча (min-heap)
    :param new_element: int, новый элемент для вставки
    :return: list, измененная куча после вставки
    """
    # Шаг 1: Добавляем новый элемент в конец кучи
    heap.append(new_element)
    index = len(heap) - 1  # Индекс нового элемента

    # Шаг 2: Восстанавливаем свойство кучи (bubble-up)
    while index > 0:
        parent_index = (index - 1) // 2  # Индекс родительского узла
        if heap[parent_index] <= heap[index]:  # Условие для min-heap
            break  # Свойство кучи восстановлено
        # Меняем местами элемент и его родителя
        heap[parent_index], heap[index] = heap[index], heap[parent_index]
        index = parent_index  # Переходим к родительскому узлу

    return heap