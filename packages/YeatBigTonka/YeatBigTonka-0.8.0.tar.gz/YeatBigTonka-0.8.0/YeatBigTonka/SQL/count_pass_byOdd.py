"""Для каждой авиакомпании посчитать количество пассажиров, перевезенных по четным и нечетным числам.
Вывод: название авиакомпании, количество пассажиров по четным дням, количество пассажиров по нечетным дням.
"""


def sql():
    a = """
        SELECT 
            c.name AS name,
            COUNT(CASE WHEN EXTRACT(DAY FROM pt.date_trip) % 2 = 0 THEN 1 END) AS cnt_even,
            COUNT(CASE WHEN EXTRACT(DAY FROM pt.date_trip) % 2 = 1 THEN 1 END) AS cnt_odd
        FROM Company c
        JOIN Trip t ON c.ID_comp = t.ID_comp
        JOIN Pass_in_trip pt ON t.trip_no = pt.trip_no
        GROUP BY c.name;

    """