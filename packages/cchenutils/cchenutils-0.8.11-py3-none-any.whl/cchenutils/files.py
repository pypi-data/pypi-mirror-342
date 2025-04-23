import csv
import os

from .dictutils import Dict


def csvwrite(fp, headers, d):
    writeheader = False if os.path.exists(fp) else True
    with open(fp, 'a', encoding='utf-8') as o:
        csvwriter = csv.DictWriter(o, fieldnames=headers, lineterminator='\n')
        if writeheader:
            csvwriter.writeheader()
        csvwriter.writerow(dict(zip(headers, Dict(d).gets(headers))))


def csvwrites(fp, headers, list_of_dicts):
    writeheader = False if os.path.exists(fp) else True
    with open(fp, 'a', encoding='utf-8') as o:
        csvwriter = csv.DictWriter(o, fieldnames=headers, lineterminator='\n')
        if writeheader:
            csvwriter.writeheader()
        for d in list_of_dicts:
            csvwriter.writerow(dict(zip(headers, Dict(d).gets(headers))))
