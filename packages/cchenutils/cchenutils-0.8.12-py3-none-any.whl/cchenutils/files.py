import csv
import json
import os

from .dictutils import Dict


def csvwrite(fp, headers, data):
    writeheader = not os.path.exists(fp)
    rows = data if isinstance(data, list) else [data]
    rows = (dict(zip(headers, Dict(d).gets(headers))) for d in rows)

    with open(fp, 'a', encoding='utf-8') as o:
        writer = csv.DictWriter(o, fieldnames=headers, lineterminator='\n')
        if writeheader:
            writer.writeheader()
        writer.writerows(rows)


def jsonwrite(fp, data):
    rows = data if isinstance(data, list) else [data]
    with open(fp, 'a', encoding='utf-8') as o:
        o.writelines(json.dumps(d) + '\n' for d in rows)
