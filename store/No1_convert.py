import csv
import datetime
import glob

def convert_utc(log_file):
    log_buffer = []
    # IpId,UserId,TimeStamp,HttpMethod,Uri,HttpVersion,ResponseCode,Bytes,Referrer,UserAgent
    with open(log_file) as f:
        reader = csv.reader(f)
        for data in reader:
            try:
                raw_time_stamp = int(data[2])
                delta = datetime.timedelta(microseconds=raw_time_stamp // 10)
                base = datetime.datetime(year=1, month=1, day=1, tzinfo=datetime.timezone.utc)
                t = base + delta
                data[2] = t.strftime("%Y/%m/%d %H:%M:%S")
                tsv = "\t".join(data)
                log_buffer.append(tsv + "\n")
                # print(log_buffer)
                # break
            except Exception as e:
                print(e)
                print(data)
                continue
    with open(log_file + ".log", mode="w") as f:
        f.writelines(log_buffer) 

file_list = glob.glob("x??")
# print(file_list)
for file_name in file_list:
    convert_utc(file_name)
