#!/usr/bin/env python3
from datetime import datetime

arrested_date = datetime(2013, 10, 1)
to_day = datetime.today()

difference_time = to_day - arrested_date

with open('/home/me/Desktop/Ross.txt', 'w') as handle:
    handle.write(
        f"""Ross Ulbricht has been in prison for {difference_time.days} days.
That's long time kiddo.
Remember it."""
)
