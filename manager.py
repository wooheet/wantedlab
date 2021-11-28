from wanted_lab.main import app, db
# from wanted_lab.main import wanted_lab
# from wanted_lab.database import SessionLocal, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
