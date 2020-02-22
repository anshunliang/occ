from flask_script import Manager
from bluelog.models import db

from flask_migrate import Migrate,MigrateCommand

from bluelog import create_app


app = create_app()
manager=Manager(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()