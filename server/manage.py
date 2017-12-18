from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app, db
from project.models.user import User

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    db.create_all()

@manager.command
def drop_db():
    db.drop_all()


if __name__ == '__main__':
    manager.run()
