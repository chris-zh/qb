import os
from werkzeug.security import generate_password_hash

qb = {}  # 全局字典


def init_qb():
    if os.path.exists('.env'):
        print('开始导入环境变量...')
        for line in open('.env'):
            if line[0:1] == '#':
                continue
            var = line.strip().split('=')
            if len(var) == 2:
                key, value = var[0].strip(), var[1].strip()
                os.environ[key] = value
        # print(os.environ.get('MAIL_SERVER'))
        print('成功！')
    else:
        print('失败！环境变量.env不存在')

if __name__ == '__main__':
    print(os.environ.values())
