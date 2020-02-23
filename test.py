from datetime import datetime

def check_hour(hour):
    if hour==0:
        hour = 23
    elif hour%2==0:
        hour = hour - 1
    return hour

txt = datetime.strptime("2017-11-09T22:00:00", '%Y-%m-%dT%H:%M:%S')
hour = txt.strftime('%H')
print(check_hour(int(hour)))
