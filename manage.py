from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from movie_trade import create_app, db

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

print(app.config['SQLALCHEMY_DATABASE_URI'])

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()