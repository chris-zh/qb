import os
from env import qb

basedir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[麻辣香锅]'  # 前缀
    FLASKY_MAIL_SENDER = qb.get('FLASKY_MAIL_SENDER')  # 服务器邮件发件人
    FLASKY_ADMIN = qb.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 5
    FLASKY_COMMENTS_PER_PAGE = 10
    UPLOAD_FOLDER = ''
    SMALL_IMAGE_SIZE = (35, 35)  # 用户小头像
    BIG_IMAGE_SIZE = (250, 250)  # 用户大头像

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    print(qb)
    # MAIL_SERVER = '10.1.190.1'
    print(qb.get('MAIL_SERVER'))
    print(qb)
    MAIL_SERVER = qb.get('MAIL_SERVER')
    MAIL_PORT = 25

    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = qb.get('MAIL_USERNAME')
    MAIL_PASSWORD = qb.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # SQLALCHEMY_BINDS = {'tpdev': 'oracle+cx_oracle://tpdev:tpdevenvpwd@10.1.101.35:1521/ORA35',
    #                     'tptstoper': 'oracle://tptstoper:tptstoperonly@10.1.101.35:1521/ORA35'}


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
