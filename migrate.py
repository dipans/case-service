from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from model import db
from run import create_app

app = create_app('config')

#Instantiates Migrate
migrate = Migrate(app, db)
#Supporting external scripting in Flask to setup database
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()