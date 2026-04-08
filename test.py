from dbhelper import DB

db=DB()
dates,flights_count=db.daily_number_of_flights()
print([type(d) for d in dates[:5]])  # should be str or datetime
print([type(v) for v in flights_count[:5]]) # should be int or float
print(dates)
print(flights_count)