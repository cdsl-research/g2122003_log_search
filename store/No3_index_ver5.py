import csv
import pathlib
import multiprocessing
import json

def create_index(file_path):
    normally_index = {}
    abnormally_index = {}

    with open(file_path, mode='r', encoding='utf-8') as f:
        offset = 0
        while True:
            line = f.readline()
            if not line:
                break  # End of file
            current_offset = offset  # Save the starting offset of the line
            cols = line.split('\t')
            key = str(cols[6])
            index = normally_index if int(cols[6]) < 400 else abnormally_index

            # キーとファイル名の辞書をセットアップ
            if key not in index:
                index[key] = {}
            if file_path.name not in index[key]:
                index[key][file_path.name] = []

            # インデックスに現在のオフセットを追加
            index[key][file_path.name].append(current_offset)
            print(file_path,current_offset, line)

            # Update the offset for the next line
            offset += len(line)

    return normally_index, abnormally_index

def merge_indices(results):
    # 結果をマージする関数
    normally_index = {}
    abnormally_index = {}

    for n_idx, ab_idx in results:
        # normally_indexをマージ
        for key, files in n_idx.items():
            if key not in normally_index:
                normally_index[key] = {}
            for file, offsets in files.items():
                if file not in normally_index[key]:
                    normally_index[key][file] = []
                normally_index[key][file].extend(offsets)

        # abnormally_indexをマージ
        for key, files in ab_idx.items():
            if key not in abnormally_index:
                abnormally_index[key] = {}
            for file, offsets in files.items():
                if file not in abnormally_index[key]:
                    abnormally_index[key][file] = []
                abnormally_index[key][file].extend(offsets)

    return normally_index, abnormally_index

if __name__ == "__main__":
    path = pathlib.Path('./')
    log_store_list = list(path.glob('**/*.tsv'))

    # プールの作成とタスクの実行
    with multiprocessing.Pool() as pool:
        results = pool.map(create_index, log_store_list)

    # 結果のマージ
    normally_index, abnormally_index = merge_indices(results)

    # インデックスの保存
    with open('normally_index_len.json', mode='w') as f:
        json.dump(normally_index, f, ensure_ascii=False)
    with open('abnormally_index_len.json', mode='w') as f:
        json.dump(abnormally_index, f, ensure_ascii=False)

