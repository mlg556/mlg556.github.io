import re
import itertools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import json

from timeit import default_timer as timer
from collections import Counter
from collections import OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from statistics import mean
from adjustText import adjust_text
from sys import argv


# extracts the title name from the url
def eksi_title_extractor(url):
    title = url.split('/')
    title = title[-1]
    title = title.split('--')
    title = title[0]
    return title


# formats seconds into hours, minutes and seconds
def sec_formatter(seconds):
    mins = int(seconds / 60)
    secs = int(seconds % 60)

    if mins >= 60:
        hours = int(mins / 60)
        mins = int(mins % 60)

        return str(hours) + 'H ' + str(mins) + 'M ' + str(secs) + 'S'

    return str(mins) + 'M ' + str(secs) + 'S'


# the url
url = argv[1]


# the top N to be annotated
top_count = 10

title_name = eksi_title_extractor(url)
log_file = title_name + '.json'

entries = []
html_dates = []
dates = []
dates_string = []
x = []
y = []
loop_times = []

url = url + '?p='

binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chromedriver_path = "REPLACE/THIS/PATH"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = binary_path

driver = webdriver.Chrome(executable_path=chromedriver_path,
                          options=chrome_options)

driver.get(url)

content = driver.page_source

regex = r'\d\d.\d\d.\d\d\d\d'

soup = BeautifulSoup(content, 'html.parser')

html_dates.append(soup.find_all("a", class_='entry-date permalink'))

attrs = soup.find(class_='pager').attrs
limit = int(attrs['data-pagecount'])  # the page count of the title

print("Pages:" + str(limit))

for i in range(2, limit + 1):

    start = timer()
    site = driver.get(url + str(i))
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    html_dates.append(soup.find_all("a", class_='entry-date permalink'))
    end = timer()

    loop_time = end-start
    loop_times.append(loop_time)
    loop_time_avg = mean(loop_times)

    print(str(i) + '/' + str(limit) + ' ----------------- %' + ("{0:.2f}".format((i/limit) * 100)))
    secs = ((limit-i)*loop_time_avg)
    print('ETA: ' + sec_formatter(secs))

html_dates = list(itertools.chain.from_iterable(html_dates))

for date in html_dates:
    result = re.findall(regex, str(date))
    dates.append(result[0])  # To avoid edit dates.

counted_dates = Counter(dates)  # counts the dates' occurrences

# dumps the results into a json for later use
with open(log_file, 'w+') as o:
    json.dump(counted_dates, o)

# the top N dates with most occurences
top = counted_dates.most_common(top_count)

# builts an ordered dict from the Counter object
counted_dates = OrderedDict(counted_dates)

for date, entry in counted_dates.items():
    dates_string.append(date)
    entries.append(entry)

for date in dates_string:
    x.append(dt.datetime.strptime(date, '%d.%m.%Y').date())

fig, ax = plt.subplots()

plt.plot(x, entries, '.')
plt.plot(x, entries)

texts = []

for i in range(top_count):
    top_x, top_y = top[i]
    texts.append(plt.text(mdates.date2num(dt.datetime.strptime(str(top[i][0]), '%d.%m.%Y').date()),
                          top[i][1], str(top[i][0]) + ', ' + str(top[i][1]), ha='right', va='top'))

adjust_text(texts)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gcf().autofmt_xdate()
plt.show()
