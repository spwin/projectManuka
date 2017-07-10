import requests
import sqlite3
from bs4 import BeautifulSoup
from generator import *

conn = sqlite3.connect('economic_calendar.db')
c = conn.cursor()

initTables(c)

start_date = initLastDate(c)
end_date = add_months(start_date, 1)
for single_date in daterange(start_date, end_date):
    print(single_date, end="")
    session = requests.Session()
    session.cookies.get_dict()

    session.headers['User-Agent'] = randomHeader()
    http = session.get('https://www.investing.com/economic-calendar/')
    session = completeHeaders(session)

    date_limits = single_date.strftime("%Y-%m-%d")

    form_data = {
        'dateFrom': date_limits,
        'dateTo': date_limits
    }
    post = session.post('https://www.investing.com/economic-calendar/Service/getCalendarFilteredData', form_data)

    response = post.json()
    data = response['data']

    # data = simulateResponse()

    html = BeautifulSoup(data, "html.parser")
    current_day = ''
    parameters = []
    for row in html.find_all('tr'):
        if len(row.find_all('td')) > 1:
            parameters.append(parseParameters(row, current_day))
        elif 'theDay' in row.find('td')['class']:
            current_day = parseDate(row.text)

    insertElements(parameters, c)

    # TODO: check if len() of all elements is 200, then post parameter limit_from += 1 and repeat

    sqlite3.time.sleep(5)
    print('OK!')
conn.commit()
c.close()
conn.close()
