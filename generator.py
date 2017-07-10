import random
import datetime
import calendar
from datetime import timedelta


def randomHeader():
    headers = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
    ]
    print('.', end="")
    return random.choice(headers)


def completeHeaders(session):
    cookies = session.cookies.get_dict()
    cookies_string = ''
    for cookie, value in cookies.items():
        cookies_string += (cookie + '=' + value + '; ')
    session.headers['Accept'] = '*/*'
    session.headers['Accept-Encoding'] = 'gzip, deflate, br'
    session.headers['Accept-Language'] = 'en-GB,en-US;q=0.8,en;q=0.6'
    session.headers['Connection'] = 'keep-alive'
    session.headers['Content-Length'] = '77'
    session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    session.headers['Cookie'] = cookies_string
    session.headers['Host'] = 'www.investing.com'
    session.headers['Origin'] = 'https://www.investing.com'
    session.headers['Referer'] = 'https://www.investing.com/earnings-calendar/'
    session.headers['X-Requested-With'] = 'XMLHttpRequest'
    print('.', end="")
    return session


def simulateResponse():
    with open('response.txt', 'r') as myfile:
        data = myfile.read()
    return data


def cleanText(text):
    return text.replace('\xa0', '').strip()


def getCurrency(td):
    td = cleanText(td.text)
    return td


def getCountry(td):
    country = cleanText(td.find('span')['title'])
    return country


def getImportance(td):
    importance = td.find_all('i', {'class': 'grayFullBullishIcon'})
    return len(importance)


def getId(tr):
    return tr['id'].split('_')[1]


def parseParameters(tr, current_day):
    counter = 0
    parameters = {
        'event_id': getId(tr),
        'time': '',
        'currency': '',
        'country': '',
        'importance': '',
        'event': '',
        'actual': '',
        'actual_title': '',
        'forecast': '',
        'previous': '',
        'previous_title': '',
        'updated_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    for td in tr.find_all('td'):
        if counter == 0:
            parameters['time'] = current_day + ' ' + td.text
        elif counter == 1:
            parameters['currency'] = getCurrency(td)
            parameters['country'] = getCountry(td)
        elif counter == 2:
            parameters['importance'] = getImportance(td)
        elif counter == 3:
            parameters['event'] = cleanText(td.text)
        elif counter == 4:
            parameters['actual'] = cleanText(td.text)
            parameters['actual_title'] = cleanText(td['title'])
        elif counter == 5:
            parameters['forecast'] = cleanText(td.text)
        elif counter == 6:
            parameters['previous'] = cleanText(td.text)
            parameters['previous_title'] = cleanText(td.find('span')['title'])
        counter += 1
    return parameters


def textToMonth(month):
    if month == 'January':
        month_counter = '01'
    elif month == 'February':
        month_counter = '02'
    elif month == 'March':
        month_counter = '03'
    elif month == 'April':
        month_counter = '04'
    elif month == 'May':
        month_counter = '05'
    elif month == 'June':
        month_counter = '06'
    elif month == 'July':
        month_counter = '07'
    elif month == 'August':
        month_counter = '08'
    elif month == 'September':
        month_counter = '09'
    elif month == 'October':
        month_counter = '10'
    elif month == 'November':
        month_counter = '11'
    else:
        month_counter = '12'
    return month_counter


def parseDate(date):
    date_parts = date.split(',')
    month_day = cleanText(date_parts[1])
    year = cleanText(date_parts[2])

    date_subparts = month_day.split(' ')
    month = date_subparts[0]
    day = str(date_subparts[1]).zfill(2)

    month = textToMonth(month)
    return year + '-' + month + '-' + day


def initTables(c):
    table_ec = 'economic_calendar'
    sql = 'create table if not exists ' + table_ec + \
          '(id integer primary key autoincrement,' \
          'event_id integer not null,' \
          'actual varchar(10),' \
          'actual_title varchar(50),' \
          'previous varchar(10),' \
          'previous_title varchar(50),' \
          'currency varchar(5),' \
          'importance int(2),' \
          'forecast varchar(10),' \
          'country varchar(20),' \
          'event varchar(255),' \
          'time varchar(19),' \
          'updated_at varchar(19))'
    c.execute(sql)
    pass


def insertElements(elements, c):
    table_ec = 'economic_calendar'
    rows = []
    for params in elements:
        rows.append([params['event_id'], params['actual'], params['actual_title'], params['previous'],
                     params['previous_title'], params['currency'], params['importance'], params['forecast'],
                     params['country'], params['event'], params['time'], params['updated_at']])
    c.executemany('insert into ' + table_ec + ' values (NULL,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
    print('.', end="")
    pass


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def initLastDate(c):
    table_ec = 'economic_calendar'
    sql = 'select time from ' + table_ec + ' order by time desc limit 1'
    c.execute(sql)
    one = c.fetchone()
    if one and one is not None:
        last_date = one[0]
    else:
        last_date = '2010-02-01 00:00'
    date = datetime.datetime.strptime(last_date, "%Y-%m-%d %H:%M").date()
    return date
