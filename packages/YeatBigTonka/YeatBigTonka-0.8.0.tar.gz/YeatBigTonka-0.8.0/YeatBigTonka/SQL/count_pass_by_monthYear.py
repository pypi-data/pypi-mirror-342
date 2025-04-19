"""Определить количество перевезенных пассажиров авиакомпаниями по месяцам и годам.
Вывод: название авиакомпании, месяц, год, число перевезенных пассажиров.
 Упорядочить результат по возрастанию года и месяца и по убыванию числа пассажиров.
"""

def sql():
    a = """
        SELECT Company.name,
	MONTH(date_trip) AS m,
	YEAR(date_trip) AS y,
	COUNT(*) AS psg
FROM Company
	JOIN Trip USING (ID_comp)
	JOIN Pass_in_trip USING (trip_no)
GROUP BY Company.name,
	m,
	y
    """


