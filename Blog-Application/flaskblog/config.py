class Config:
    SECRET_KEY = "any secret key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'hafsaamanan@gmail.com'
    MAIL_PASSWORD = 'ybnshqivxejlwethif'
    MAIL_DEFAULT_SENDER = 'hafsaamanan@gmail.com'

    #set private information in the form of environment variables
    #then do os.environ.get("name_of_the_variable")
