"""Для всех городов из таблицы Trip посчитать количество вылетов и прилетов за апрель 2025 года.
"""

def sql():
    a = """WITH t1 AS (
	SELECT Trip.trip_no,
		Trip.town_from,
		Trip.town_to,
		date_trip
	FROM Trip
		LEFT JOIN Pass_in_trip Pit ON Trip.trip_no = Pit.trip_no
	WHERE date_trip BETWEEN '2025-04-01' AND '2025-04-30'
	GROUP BY Trip.trip_no,
		Trip.town_from,
		Trip.town_to,
		date_trip
),
t2 AS (
	SELECT t1.town_from as tw,
		COUNT(t1.town_from) as ct_out
	FROM t1
	GROUP BY t1.town_from
),
t3 AS (SELECT t1.town_to as tw,
              COUNT(t1.town_to) as ct_in
       FROM t1
       GROUP BY t1.town_to)

SELECT t2.tw, t2.ct_out, t3.ct_in FROM t2
join t3 on t2.tw = t3.tw
    """

