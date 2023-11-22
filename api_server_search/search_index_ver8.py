from fastapi import FastAPI
from typing import List
import uvicorn
import json
import multiprocessing
import csv

abnormally_index = {}

with open('abnormally_index.json') as f:
    abnormally_index = json.load(f)


def search(block_name, index_list):
    result = []
    with open(block_name, encoding='utf-8', newline='') as f:
        file = list(csv.reader(f, delimiter='\t'))
        for j in index_list:
            result.append(file[j])
    return result

# 検索を並列処理で実行
def perform_parallel_search(index_results):
    # 使用可能なプロセス数を取得
    available_cpus = multiprocessing.cpu_count()
    # 使用するプロセス数を決定（利用可能なCPUコア数と、分割されたファイル数の小さい方）
    num_processes = min(available_cpus, len(index_results))

    # プロセスプールを作成
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 並列処理を実行するための引数のリストを作成
        tasks = [(block_name, index_list) for block_name, index_list in index_results.items()]
        # 並列処理を実行
        results = pool.starmap(search, tasks)

    return results

app = FastAPI()

status_list = [400,401,402,403,404,500,501,502]

@app.post("/search_abnormally")
async def search_abnormally() -> List:
    merged_results = {}
    #for key in status_list:
    for key, value in abnormally_index.items():
        if int(key) >= 500:
            #for file_name, index_list in abnormally_index[key].items():
            for file_name, index_list in value.items():
                if file_name not in merged_results:
                    merged_results[file_name] = []
                merged_results[file_name].extend(index_list)
    
    # 重複を削除し、ソート
    for file_name, index_list in merged_results.items():
        merged_results[file_name] = sorted(set(index_list))

    print("start")
    index_results = merged_results

    # 並列処理を実行
    results = perform_parallel_search(index_results)

    # 結果のリストを結合
    all_results = []
    for result in results:
        all_results.extend(result)

    # サブリストの2番目の要素である時刻で降順にソート
    sorted_results = sorted(all_results, key=lambda x: x[2], reverse=True)
    return sorted_results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

