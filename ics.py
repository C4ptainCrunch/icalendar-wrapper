import icalendar
import arrow

class Calendar(object):
    """docstring for Calendar"""
    def __init__(self, from_string=None):
        if not from_string:
            self.icalendar = icalendar.Calendar()
        else:
            self.icalendar = icalendar.Calendar.from_ical(from_string)

        self.icalendar['VERSION'] = "2.0"

    def _get_stripped_prop_or_none(self, property):
        value = self.icalendar.get(property, None)
        if value is None:
            return None
        return value.__str__().strip()

    @property
    def creator(self):
        return self._get_stripped_prop_or_none('PRODID')

    @creator.setter
    def creator(self, value):
        self.icalendar['PRODID'] = str(value)


    def __str__(self):
        # TODO : should be moved to a 'pre_print' fn
        if self.creator is None:
            self.creator = 'ics.py//http://github.com/C4ptainCrunch/ics.py'
        return self.icalendar.to_ical()

    def __repr__(self):
        return "<Calendar with {} events>".format(len(self.events()))

    def events(self):
        walk = self.icalendar.walk()
        def ievent_to_event(ievent):
            event = Event(ievent)
            return event
        ievents = filter(lambda x: type(x) is icalendar.cal.Event, walk)
        events = map(ievent_to_event, ievents)

        return events

    def add_event(self, event=None):
        if event is None:
            event = Event()
        assert type(event) is Event

        ievent =  event._ievent
        self.icalendar.add_component(ievent)

        return event


class Event(object):
    """docstring for Event"""
    def __init__(self,ievent=None):
        if not ievent:
            ievent = icalendar.Event()
        self._ievent = ievent

    @property
    def start(self):
        start = self._ievent.get('DTSTART', None)
        if start is None:
            return None
        return arrow.Arrow.fromdatetime(start.dt)

    @start.setter
    def start(self, value):
        if type(value) is arrow.Arrow:
            value = value.datetime
        # TODO : raise if canot cast value to a datetime
        self._ievent['DTSTART'].dt = value


    @property
    def end(self):
        end = self._ievent.get('DTEND', None)
        if end is None:
            return None
        return arrow.Arrow.fromdatetime(end.dt)

    @end.setter
    def end(self, value):
        if type(value) is arrow.Arrow:
            value = value.datetime
        # TODO : raise if canot cast value to a datetime
        self._ievent['DTEND'].dt = value

    @property
    def name(self):
        return self._get_stripped_prop_or_none('SUMMARY')

    @name.setter
    def name(self, value):
        self._ievent['SUMMARY'] = str(value)

    @property
    def location(self):
        return self._get_stripped_prop_or_none('LOCATION')

    @location.setter
    def location(self, value):
        self._ievent['LOCATION'] = str(value)

    @property
    def categories(self):
        categories = self._ievent.get('CATEGORIES', [])
        if not categories == []:
            categories = map(lambda x: x.strip(), categories.split(','))
        return categories

    @categories.setter
    def categories(self, value):
        self._ievent['CATEGORIES'] = ','.join(value)

    @property
    def status(self):
        return self._get_stripped_prop_or_none('STATUS')

    @status.setter
    def status(self, value):
        # TODO : raise if not in (TENTATIVE, CONFIRMED, CANCELLED)
        self._ievent['STATUS'] = str(value)

    @property
    def description(self):
        return self._get_stripped_prop_or_none('DESCRIPTION')

    @description.setter
    def description(self, value):
        self._ievent['DESCRIPTION'] = str(value)

    @property
    def busy(self):
        return self._get_stripped_prop_or_none('TRANSP')

    @busy.setter
    def busy(self, value):
        # TODO : raise if not in  (OPAQUE, TRANSPARENT)
        self._ievent['TRANSP'] = str(value)

    @property
    def sequence(self):
        seq = self._ievent.get('SEQUENCE', None)
        if seq is None:
            return 0
        return int(seq)

    @sequence.setter
    def sequence(self, value):
        # TODO : better cast
        self._ievent['SEQUENCE'] = str(int(value))

    @property
    def url(self):
        return self._get_stripped_prop_or_none('URL')

    @url.setter
    def url(self, value):
        self._ievent['URL'] = str(value)

    def _get_stripped_prop_or_none(self, property):
        value = self._ievent.get(property, None)
        if value is None:
            return None
        return value.__str__().strip()

    def __repr__(self):
        string = "<Event"
        if self.name:
            string += " {}".format(self.name)

        if self.start:
            string += " from {}".format(self.start.format('DD-MM-YY HH:mm'))

        if self.end:
            string += " to {}".format(self.end.format('DD-MM-YY HH:mm'))

        return string + ">"

    def __str__(self):
        return self._ievent.to_ical()
