ics.py
=====

`ics.py` is a pythonic library to read, create and modify icalendar/ics files (as described in [rfc2445 bis](http://tools.ietf.org/html/draft-ietf-calsify-rfc2445bis-08) and used by Google cal, Apple calendar, Sunbird, ... )

`ics.py` is wrapper aroud the [icalendar](https://pypi.python.org/pypi/icalendar) python lib


Usage
----

```python
import ics

calendar = ics.Calendar()
calendar.events # Return a list of ics.Events()

event = calendar.add_event()
event.name = 'My cool hackathon'
event.start = start_time # Give a datetime or Arrow object
event.end = end_time # Give a datetime or Arrow object

# Lot of other properties avalable

event2 = Event()
event2.name = 'My cool lan party'
calendar.add_event(event2)

open('mah_calendar.ics','w').write(str(calendar))

calendar2 = ics.Calendar(open('mah_other_calendar.ics','r').read())
calendar2.events[0].name = 'Change event name'
open('mah_other_calendar.ics','w').write(str(calendar2))
```

Limitations
---

`ics.py` supports only events and every property is not supported.
(for example, recurrent events are not supported)