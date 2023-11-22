# g2122003_log_search
アクセスログを保存して検索するものです．
EClog用にカスタマイズしています．

storeに保存しているNo1\_convert.py  No2\_method\_store.py  No3\_index\_ver5.pyを実行します．
```shell
$ ls
eclog.csv No1\_convert.py  No2\_method\_store.py  No3\_index\_ver5.py
```

```shell
$ python3 No1_convert.py
```
```shell
$ python3 No2_method_store.py 
```
```shell
$ python3 No3_index_ver5.py
```

api\_server\_searchにindexとログを移動させて検索のAPIを起動します．
```shell
$ ls
abnormally_index.json abnormally_list000.tsv requirements.txt startunicon.sh search_index_ver8.py
```

起動
```shell
$ ./startunicon.sh
```
