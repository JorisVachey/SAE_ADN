#>>>import random, string, os
#>>>"".join([random.choice(string.printable) for _ in os.urandom(24) ] )
SECRET_KEY = "5fef1b93-18c5-4645-83e3-af53523a3e28"
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'monApp.db')