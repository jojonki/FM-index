# FM-index
The Burrows–Wheeler transform (also called block-sorting compression) 

## How to Use
```
Directory Search base
$ python main.py -d /path/to/doc/dir -q query-you-want-to-search

File base
$ python main.py -f /path/to/doc.txt -q query-you-want-to-search

Server mode
$ python server.py --dict index.dict --dir /path/to/doc_dir-or-txt
```
