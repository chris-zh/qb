import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 分页设置
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 5
    FLASKY_COMMENTS_PER_PAGE = 10
    # 头像尺寸设置
    SMALL_IMAGE_SIZE = (35, 35)  # 用户小头像
    BIG_IMAGE_SIZE = (250, 250)  # 用户大头像
    # 管理员邮箱设置 在.env中配置
    FLASKY_MAIL_SUBJECT_PREFIX = '[麻辣香锅]'  # 前缀
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')  # 服务器邮件发件人
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  # 服务器管理员邮箱
    MAIL_SERVER = os.environ.get('MAIL_SERVER')  # 发件服务器
    MAIL_PORT = os.environ.get('MAIL_PORT')  # 发件服务器端口
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 服务器管理员账号
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 服务器管理员密码
    MAIL_USE_TLS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
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
