"""Для каждой авиакомпании посчитать количество перевезенных пассажиров по типам самолетов.
Вывод: название авиакомпании, тип самолета, количество перевезенных пассажиров.
"""

def sql():
    a = """
        SELECT Company.name,Trip.plane, COUNT(Pass_in_trip.ID_psg) From Company
join Trip on Company.ID_comp = Trip.ID_comp
join Pass_in_trip on Trip.trip_no = Pass_in_trip.trip_no
GROUP BY Trip.plane, Company.name
    """