import os
from env import init_qb
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 初始化全局变量
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

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.host = '0.0.0.0'
manager = Manager(app)
migrate = Migrate(app, db)

from flask_login import login_required


@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    manager.run()
