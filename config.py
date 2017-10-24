import os

class Config:
    SECRET_KEY = os.environ.get('CSUSB_SECRET', 'secret-key')
    SQLALCHEMY_DATABASE_URI = 'postgres://ituakzqmjbmznp:eFvtMtJEl1UtfAq6p0gD-a4e5G@ec2-54-221-234-118.compute-1.amazonaws.com:5432/d6lbbjl7ggnlpr'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    UPLOAD_FOLDER = 'csusb/static/img/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
}
