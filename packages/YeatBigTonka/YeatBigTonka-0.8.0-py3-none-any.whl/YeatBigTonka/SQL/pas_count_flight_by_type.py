"""Для каждого пассажира определить количество полетов по типам самолетов.
Вывод: имя пассажира, тип самолета, количество перелетов этим типом самолета. Результат упорядочить по именам пассажиров (в алфавитном порядке) и убыванию количества перелетов.
Примечание: Задача «с подвохом» в БД есть полные тезки (Bruce Willis), они отличаются кодом (Id_psg), поэтому группировать результат надо не по имени пассажира, а по его коду
"""

def sql():
    a = """
       with t1 as (SELECT Passenger.ID_psg, Passenger.name, Pass_in_trip.trip_no, Trip.plane
            FROM Passenger
                     join Pass_in_trip using (ID_psg)
                     join Trip using (trip_no)
            )
SELECT t1.name, t1.plane, COUNT(t1.trip_no) FROM t1
GROUP BY t1.ID_psg, t1.plane
order by name
    """