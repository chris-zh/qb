import os

qb = {}  # 全局字典


def init_qb():
    if os.path.exists('.env'):
        print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            qb[var[0]] = var[1]
