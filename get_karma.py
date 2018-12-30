from pytodoist import todoist

user1 = todoist.login('todoistloginemail@domain.com', 'password')

import datetime as dt
today = dt.datetime.today().strftime('%d-%b-%Y')
data=[today, user1.karma]

import csv 
csvfile = open('karma.csv', 'ab')
write_pattern = csv.writer(csvfile, delimiter=",", quotechar=",")
write_pattern.writerow(data)
csvfile.close()
