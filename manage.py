import os
from env import init_qb
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

init_qb()  # 初始化全局变量
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
