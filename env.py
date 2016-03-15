import os
from werkzeug.security import generate_password_hash

qb = {}  # 全局字典


def init_qb():
    if os.path.exists('.env'):
        print('Importing environment from .env...')
    for line in open('.env'):
        if line[0:1] == '#':
            continue
        var = line.strip().split('=')
        print(var)
        if len(var) == 2:
            key, value = var[0].strip(), var[1].strip()
            os.environ[key] = value
    print(os.environ.get('MAIL_SERVER'))


if __name__ == '__main__':
    init_qb()
