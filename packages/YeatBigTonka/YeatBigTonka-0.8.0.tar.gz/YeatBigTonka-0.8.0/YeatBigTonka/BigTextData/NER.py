# Проведите анализ текстовых сущестной (решите задачу NER). Результат работы программы должен выглядеть:
#
#
#
# Реализуйте функцию, которую можно дать на вход text, а она вернет размеченный текст.
# Дополнительное задание:
# улучшите функцию, добавь в качестве переменной тип именной сущности. Результатом отработки функции должен быть список частей текста, соответствующей сущности в именительном падеже.
# Пример
# print(mu_ner(text, “ORG”) )
# [Абаканский линейный отдел, МВД ]

# !pip install natasha pymorphy2

from natasha import (
    Segmenter,
    MorphTagger,
    NewsNERTagger,
    NewsMorphTagger,
    Doc
)
from pymorphy2 import MorphAnalyzer

# Инициализация необходимых объектов Natasha
segmenter = Segmenter()
morph_tagger = NewsMorphTagger()
ner_tagger = NewsNERTagger()
morph_syntax_tagger = MorphTagger()  # Альтернатива NewsMorphTagger
morph_analyzer = MorphAnalyzer()  # Для проверки и приведения к начальной форме

text = (
    "Инцидент произошел на перегоне Туманный — Ербинская. Внимательный машинист "
    "заметил, что на рельсах что-то лежит, и сообщил об этом в дежурную часть "
    "Абаканского линейного отдела МВД РФ. Прибывшая на место происшествия "
    "следственно-оперативная группа вскрыла мешок и обнаружила в нем щенков."
)


def ner_markup(text: str) -> str:
    """
    Размечает в исходном тексте именованные сущности, оборачивая их в теги [TYPE]...[/TYPE].
    Возвращает строку с разметкой.
    """
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    # Пройдёмся по сущностям, чтобы "обернуть" их в теги
    # Например, [LOC]Туманный[/LOC]
    entities = doc.spans  # все распознанные сущности
    # Важно: чтобы при замене не сместились индексы, менять текст лучше с конца к началу.
    if not entities:
        return text  # ничего не найдено

    # Сортируем сущности по началу (в убывающем порядке), чтобы вставлять теги справа налево
    entities = sorted(entities, key=lambda x: x.start, reverse=True)

    marked_text = text
    for span in entities:
        # Например, span.type = 'LOC', span.text = 'Туманный'
        start, stop = span.start, span.stop
        ent_type = span.type
        # Добавляем теги: [LOC]Туманный[/LOC]
        marked_text = (
                marked_text[:start]
                + f"[{ent_type}]" + span.text + f"[/{ent_type}]"
                + marked_text[stop:]
        )

    return marked_text


def mu_ner(text: str, entity_type: str) -> list[str]:
    """
    Возвращает *список* фрагментов текста заданного типа (например, 'ORG'),
    преобразованных по возможности к именительному падежу.

    Пример: mu_ner(text, "ORG") -> ["Абаканский линейный отдел", "МВД РФ"] (может отличаться в зависимости от NER)
    """
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    results = []
    if not doc.spans:
        return results

    for span in doc.spans:
        if span.type == entity_type:
            # span.text — исходный фрагмент
            # Попробуем для каждого слова внутри span.text привести к начальной (лексической) форме,
            # а затем постараемся согласовать в именительном падеже (не всегда точно)
            normalized = convert_to_nominative(span.text)
            results.append(normalized)

    return results


def convert_to_nominative(phrase: str) -> str:
    """
    Утилита для грубого приведения словосочетания к именительному падежу.
    Для упрощения: разбиваем по пробелам, каждое слово приводим к лексической форме
    (Parse.normal_form), а затем просим pymorphy подобрать слово в именительном падеже.
    В случаях типа "Абаканского линейного отдела" может получиться неточная форма,
    но для демонстрации принципа хватит.
    """
    words = phrase.split()
    result_words = []

    for w in words:
        # Находим все возможные разборы
        parses = morph_analyzer.parse(w)
        if not parses:
            result_words.append(w)
            continue

        # Берём самый вероятный разбор
        best_parse = parses[0]
        # Приводим к нормальной форме (например, "Абаканский" из "Абаканского")
        normal = best_parse.normal_form

        # Пробуем задать грамему именительного падежа, единственного числа (или как будет)
        # Задаём желаемые грамемы: {'sing', 'nomn'} = единственное число, именительный падеж
        # (для аббревиатур, возможно, это не применимо)
        nominative_parse = best_parse.inflect({'nomn'})  # Применяем только именит. падеж
        if nominative_parse:
            # Если получилось, берём словоформу
            word_in_nom = nominative_parse.word
            result_words.append(word_in_nom)
        else:
            # Если не получилось, вставляем нормальную форму
            result_words.append(normal)

    # Склеиваем обратно в строку
    return " ".join(result_words)


# ====================== Пример использования ======================
if __name__ == "__main__":
    print("=== Пример разметки NER ===")
    marked = ner_markup(text)
    print(marked)
    # Могут получиться теги вида [LOC]Туманный[/LOC], [ORG]МВД РФ[/ORG] и т.д.

    print("\n=== Пример выборки сущностей ORG в именительном падеже ===")
    org_list = mu_ner(text, "ORG")
    print(org_list)

    print("\n=== Пример выборки сущностей LOC в именительном падеже ===")
    loc_list = mu_ner(text, "LOC")
    print(loc_list)
