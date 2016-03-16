from app.models import Role
import os


def init_roles():
    Role.insert_roles()


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


# 调用
def run_scripts():
    init_roles()


if __name__ == '__main__':
    run_scripts()
