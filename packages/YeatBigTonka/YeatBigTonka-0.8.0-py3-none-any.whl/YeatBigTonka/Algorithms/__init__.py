# Напишите программу, которая получает число в двоичной системе и преобразует его в десятеричную и шестнадцатеричную системы счисления.
from .convert_binary_to_decimal_and_hex import convert_binary_to_decimal_and_hex

# Напишите функцию, которая принимает на вход бинарную кучу и новый элемент, который нужно вставить. Функция должна вставить элемент в кучу и вернуть измененную кучу.
from .insert_into_heap import insert_into_heap

# Напишите функцию, которая принимает на вход массив целых чисел и сортирует его методом слияния.
from .merge_sort import merge_sort

# Напишите программу, которая запрашивает у пользователя два комплексных числа в формате a + i*b и выводит на экран их сумму, разность и произведение в виде кортежа. Для решения этой задачи НЕЛЬЗЯ :) использовать встроенный тип данных complex.
from .parse_complex import parse_complex

# Напишите функцию, которая принимает на вход односвязный список и индекс элемента, который нужно удалить. Функция должна удалить элемент с указанным индексом и вернуть измененный список.
from .remove_node_at_index import remove_node_at_index

# Напишите программу, которая запрашивает у пользователя строку и выводит на экран долю гласных букв в этой строке.
from .vowel_fraction import vowel_fraction

from.bubble_sort import bubble_sort

__add__ = ['convert_binary_to_decimal_and_hex', 'insert_into_heap', 'merge_sort', 'parse_complex',
           'remove_node_at_index', 'vowel_fraction', 'bubble_sort']
