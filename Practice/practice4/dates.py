# dates.py

from datetime import datetime, timedelta

# current date
now = datetime.now()
print(now)

# create date
my_date = datetime(2024, 1, 1)
print(my_date)

# format date
print(now.strftime("%Y-%m-%d"))

# difference between dates
diff = now - my_date
print(diff.days)

# add days
new_date = now + timedelta(days=10)
print(new_date)