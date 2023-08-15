from datetime import datetime
time = '3 Oct 2016 17:00:10'
t = datetime.strptime(time, "%d %b %Y %H:%M:%S")
print (t)