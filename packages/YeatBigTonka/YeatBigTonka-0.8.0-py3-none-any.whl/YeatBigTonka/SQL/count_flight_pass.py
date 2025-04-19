"""
Для каждого рейса посчитать количество полетов и перевезенных пассажиров.
Вывод: № рейса, название авиакомпании, город вылета, город прилета, количество полетов, количество перевезенных пассажиров.
Примечание: Исходя из схемы данных, любой рейс может быть не чаще одного раза в сутки (время вылета задается в таблице Trip в поле time_out, а дата – в таблице Pass_in_trip в поле date_trip). Таким образом количество полетов – это количество уникальных дат для рейса в таблице Pass_in_trip, а число пассажиров – количество строк для рейса в той же таблице.

"""
def sql():
    a = """
        SELECT 
            t.trip_no,
            c.name AS name,
            t.town_from,
            t.town_to,
            COUNT(DISTINCT pt.date_trip) AS cnt_trip,
            COUNT(*) AS cnt_psg
        FROM Trip t
        JOIN Company c ON t.ID_comp = c.ID_comp
        JOIN Pass_in_trip pt ON t.trip_no = pt.trip_no
        GROUP BY t.trip_no, c.name, t.town_from, t.town_to
        ORDER BY t.trip_no;


    """