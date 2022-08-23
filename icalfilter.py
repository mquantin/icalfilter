import icalendar
import datetime
import pytz
import logging

logging.basicConfig(filename='filter.log',  level=logging.DEBUG)

utc = pytz.utc

YEAR = 2022
MONTH = 9
DAY = 1



def main():
    with open('in.ics', 'r', encoding='utf-8') as f:
        cal = icalendar.Calendar.from_ical(f.read())
        outcal = icalendar.Calendar()

        for name, value in cal.items():
            outcal.add(name, value)

        def active_event(item):
            start_date = item['dtstart'].dt

            # recurrent
            if 'RRULE' in item:
                rrule = item['RRULE']
                # print (rrule)
                if 'UNTIL' not in rrule:
                    return True
                else:
                    assert len(rrule['UNTIL']) == 1
                    until_date = rrule['UNTIL'][0]

                    if type(until_date) == datetime.datetime:
                        return until_date >= utc.localize(datetime.datetime(YEAR, MONTH, DAY))

                    if type(until_date) == datetime.date:
                        return until_date >= datetime.date(YEAR, MONTH, DAY)

                    raise Exception('Unknown date format for "UNTIL" field')

            # not reccurrent
            if type(start_date) == datetime.datetime:
                return start_date >= utc.localize(datetime.datetime(YEAR, MONTH, DAY))

            if type(start_date) == datetime.date:
                return start_date >= datetime.date(YEAR, MONTH, DAY)

            raise Exception('ARGH')


        includedCnt = 0
        excludedCnt = 0
        for item in cal.subcomponents:
            if item.name == 'VEVENT':
                start_date = item['dtstart'].dt
                if active_event(item):
                    includedCnt +=1
                    logging.info(str('INCLUDE ' + repr(start_date) + ' ' + item['summary']))
                    outcal.add_component(item)
                else:
                    excludedCnt +=1
                    logging.info(str('EXCLUDE ' + repr(start_date) + ' ' + item['summary']))
                    pass
            else:
                logging.info('SPECIAL_INCLUDE', item)
                outcal.add_component(item)

        with open('out.ics', 'wb') as outf:
            outf.write(outcal.to_ical(sorted=False))
        print ('Included events: ', includedCnt,'\nExcluded events: ', excludedCnt)

main()
