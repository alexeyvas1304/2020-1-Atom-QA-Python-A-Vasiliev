import argparse
import os
from collections import defaultdict
import json

parser = argparse.ArgumentParser(description='nginx logger')
parser.add_argument('dir', type=str, help='dir for logs')
parser.add_argument('--file', type=str,
                    help='file for logs')
parser.add_argument('--jsonify', type=str,  # с bool не вышло
                    help='jsonify result or not')
args = parser.parse_args()


class BadFileException(Exception):
    pass


def analysis(filename, jsonify=False):
    with open(filename, 'r') as f:
        lst_of_logs = f.read().splitlines()

    d_for_json = dict()
    d_for_json['Top-10 requests on size'] = []
    d_for_json['Top-10 client errors on frequency'] = []
    d_for_json['Top-10 client errors on size'] = []

    with open(f'{filename.split("/")[-1].split(".")[0]}_analysis.txt', 'w') as f:

        f.write(f"Total requests: {len(lst_of_logs)}\n")
        if jsonify:
            d_for_json['Total requests'] = len(lst_of_logs)

        lst_of_logs = list(map(lambda x: x.split(), lst_of_logs))
        d_methods = defaultdict(int)

        for log in lst_of_logs:
            d_methods[log[5][1:]] += 1
        for k, v in d_methods.items():
            f.write(f"{k} is repeated {v} times\n")
            if jsonify:
                d_for_json[k] = v

        f.write("Top-10 requests on size:\n")
        lst = sorted(lst_of_logs, key=lambda x: -int(x[9]))[:10]
        for log in lst:
            f.write(f"url:{log[6]} status_code:{log[8]} size:{log[9]}\n")
            if jsonify:
                d_for_json['Top-10 requests on size'].append(
                    {'ip': log[0], 'url': log[6], 'status_code': log[8], 'size': log[9]})

        f.write("Top-10 client errors on frequency:\n")
        lst_of_logs_client_errors = list(filter(lambda x: x[8].startswith('4'), lst_of_logs))
        d_errors = defaultdict(int)
        for log in lst_of_logs_client_errors:
            d_errors[(log[6], log[8])] += 1
        d_errors_list = list(d_errors.items())
        d_errors_list = sorted(d_errors_list, key=lambda x: -x[1])[:10]
        for elem in d_errors_list:
            f.write(f"{elem[0][0]} status_code:{elem[0][1]} is repeated {elem[1]} times\n")
            if jsonify:
                d_for_json['Top-10 client errors on frequency'].append(
                    {'url': elem[0][0], 'status_code': elem[0][1], 'number': elem[1]})

        f.write("Top-10 client errors on size:\n")
        lst = sorted(lst_of_logs_client_errors, key=lambda x: -int(x[9]))[:10]
        for log in lst:
            f.write(f"ip:{log[0]} url:{log[6]} status_code:{log[8]} size:{log[9]}\n")
            if jsonify:
                d_for_json['Top-10 client errors on size'].append(
                    {'ip': log[0], 'url': log[6], 'status_code': log[8], 'size': log[9]})

        if jsonify == 'True':
            with open(f'{filename.split("/")[-1].split(".")[0]}_analysis.json', 'w') as f:
                json.dump(d_for_json, f, ensure_ascii=False)


if args.file:
    filename = os.path.join(args.dir, args.file)
    try:
        analysis(filename, jsonify=args.jsonify)
    except Exception:
        raise BadFileException(f'file {filename} has problems')

else:
    for file in os.listdir(args.dir):
        filename = os.path.join(args.dir, file)
        try:
            analysis(filename, jsonify=args.jsonify)
        except Exception:
            raise BadFileException(f'file {filename} has problems')
