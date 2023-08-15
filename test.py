from datetime import datetime
import pytz

time = '3 Oct 2016 17:00:10'
# converts string to datetime
pubtime = datetime.strptime(time, "%d %b %Y %H:%M:%S")
# changes timezone
pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
print (pubtime.tzinfo)

