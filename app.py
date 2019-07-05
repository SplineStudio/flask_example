from config import DevConfig
from flask_migrate import MigrateCommand
from flask_script import Manager

from project import create_app

app = create_app()
app.config.from_object(DevConfig)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

