
"""Для пассажиров летавших у окна (места a или d) вывести следующую информацию: имя пассажира, название авиакомпании,
 дата и время вылета (одно значение), город вылета, город прилета.
"""
def sql():
    a = """
        SELECT Passenger.name,
       Company.name,
       concat(Pass_in_trip.date_trip,' ', Trip.time_out) as dt_out,
       Trip.town_from,
       Trip.town_to
FROM Passenger
join Pass_in_trip On Passenger.ID_psg = Pass_in_trip.ID_psg
join Trip on Pass_in_trip.trip_no = Trip.trip_no
join Company on Trip.ID_comp = Company.ID_comp
WHERE Pass_in_trip.place LIKE '%a' OR Pass_in_trip.place LIKE '%d'
    """