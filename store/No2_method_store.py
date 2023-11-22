import sys
import pathlib
import pprint
import csv
import os
import multiprocessing

# 引数で値をとる（没案）
#args = sys.argv
#print(args)
#print(args[0])

path = pathlib.Path('./')
# **: directory **/*: file
log_file_list = path.glob('**/*.log')
sorted_log_file_list = sorted(list(log_file_list))
pprint.pprint(sorted_log_file_list)

# ログの分割数はCPUのコア数
division_number = len(os.sched_getaffinity(0))
print("division_number:", division_number)
print("multiprocessing.cpu_count():", multiprocessing.cpu_count())

normally_count = 0
abnormally_count = 0

for i in sorted_log_file_list:

    normally_list = [[] for i in range(division_number)]
    abnormally_list = [[] for i in range(division_number)]

    with open(i, encoding='utf-8', newline='') as f:

        # ログを正常系と異常系に分ける
        for cols in csv.reader(f, delimiter='\t'):
            if int(cols[6]) < 400:
                normally_list[normally_count].append(cols)
                # ログは１件ずつ分ける
                normally_count += 1
                normally_count %= division_number
            else:
                abnormally_list[abnormally_count].append(cols)
                # ログは１件ずつ分ける
                abnormally_count += 1
                abnormally_count %= division_number

# デバック用のprint文
#    print(i)
#    for i in range(division_number):
#        print("normally_list[", i,"]", len(normally_list[i]), sys.getsizeof(normally_list[i]), "byte")
#        print("abnormally_list[", i, "]", len(abnormally_list[i]), sys.getsizeof(abnormally_list[i]), "byte")

    # メモリに配列を溜めておくとメモリが足りなくなるので，読み取ったファイルごとに書き込むことにした
    for j in range(division_number):
        with open("normally_list"+str(j).zfill(3)+".tsv", mode='a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(normally_list[j])
            normally_list[j] = [] 
        with open("abnormally_list"+str(j).zfill(3)+"tsv", mode='a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(abnormally_list[j])
            abnormally_list[j] = [] 




