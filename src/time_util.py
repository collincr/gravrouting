import datetime
import time

def main():
    FMT = '%H:%M:%S'
    times_origin = ["08:31:29", "5:50:57", "9:12:32", "7:20:35", "6:18:55", "6:16:04", "6:15:04", "4:00:40"]
    times_agglomerative = ["7:45:39", "7:08:35", "7:52:48", "7:28:16", "7:58:01", "7:47:51", "2:17:59"]
    times_aggregated = ["7:55:51", "7:35:27", "7:47:29", "7:12:39", "7:10:49", "7:05:43", "7:23:31"]
    get_total_time(times_origin)
    get_total_time(times_agglomerative)
    get_total_time(times_aggregated)
    pass

def get_total_time(times):
    total_time = 0
    for period in times:
        #total_time = datetime.datetime.strptime(total_time, FMT) + datetime.datetime.strptime(time, FMT)
        x = time.strptime(period.split(',')[0],'%H:%M:%S')
        t = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        total_time += t
        #print(t)
    print("total_time", datetime.timedelta(seconds=total_time), "(", total_time, "sec)")

if __name__ == '__main__':
    main()
