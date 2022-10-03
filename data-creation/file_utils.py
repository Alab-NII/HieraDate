"""
    -*- coding: utf-8 -*-
    Basic read/write of files
    Thanks Khoa Duong for the suggestion and sharing the original file
"""
import json
import os
import csv

def make_dirs(dirname):
    if dirname:
        os.makedirs(dirname, exist_ok=True)


def read_file(filename):
    with open(filename, mode="rb") as f:
        return f.read()


def write_file(data, filename):
    make_dirs(os.path.dirname(filename))
    with open(filename, mode="wb") as f:
        f.write(data)


def read_text(filename, encoding="UTF-8"):
    with open(filename, mode="r", encoding=encoding) as f:
        return f.read()


def write_text(text, filename, encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    with open(filename, mode="w", encoding=encoding) as f:
        f.write(text)


def read_lines(filename, encoding="UTF-8"):
    with open(filename, mode="r", encoding=encoding) as f:
        for line in f:
            yield line.rstrip("\r\n\v")


def write_lines(lines, filename, linesep="\n", encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    with open(filename, mode="w", encoding=encoding) as f:
        for line in lines:
            f.write(line)
            f.write(linesep)


def read_json(filename, encoding="UTF-8"):
    with open(filename, mode="r", encoding=encoding) as f:
        return json.load(f)


def read_json_with_key(fn, key="id", encoding="UTF-8"):
    """
        - each line is a json
        - without indent
    """
    dic = {}
    with open(fn, "r", encoding=encoding) as f:
        for line in f:
            obj = json.loads(line)
            dic[obj[key]] = obj
    return dic


def read_json_with_key_special(fn, key="id", encoding="UTF-8"):
    """
        - key is a list, need to convert first
    """
    dic = {}
    with open(fn, "r", encoding=encoding) as f:
        for line in f:
            obj = json.loads(line)
            if len(obj[key]) > 1: 
                for idx in range(len(obj[key])):
                    dic[obj[key][idx]] = obj
            else:
                dic[obj[key][0]] = obj
    return dic


def write_json(obj, filename, indent=None, encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    with open(filename, mode="w", encoding=encoding) as f:
        json.dump(obj, fp=f, ensure_ascii=False, indent=indent)


def read_json_lines(filename, encoding="UTF-8"):
    for json_line in read_lines(filename, encoding=encoding):
        yield json.loads(json_line)


def read_json_lines_return_list(filename, encoding="UTF-8"):
    """
        - each line is a json
        - without indent
    """
    list_ = []
    with open(filename, "r", encoding=encoding) as f:
        for line in f:
            list_.append(json.loads(line))
    return list_


def write_json_lines(lines, filename, linesep="\n", encoding="UTF-8"):
    json_lines = (json.dumps(line, ensure_ascii=False) for line in lines)
    write_lines(json_lines, filename=filename, linesep=linesep, encoding=encoding)


def write_jsonl_format(data, filename, indent=None, encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    with open(filename, 'w', encoding=encoding) as f:
        print ("Saving {}".format(filename))
        json.dump({'data': data}, f)
        

def write_jsonl_format_without_key(data, filename, indent=None, encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    with open(filename, 'w', encoding=encoding) as f:
        print ("Saving {}".format(filename))
        json.dump(data, f)
    

def write_csv(data, filename, encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    # 
    with open(filename, 'w') as f:
        csv_out = csv.writer(f)
        for row in data:
            csv_out.writerow(row)


def write_dict(data, filename, encoding="UTF-8"):
    make_dirs(os.path.dirname(filename))
    # 
    f = open(filename, "w", encoding=encoding)
    #
    for k, v in data.items():
        f.write("{}\t{}\n".format(k, v))    
    f.close()
    