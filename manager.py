from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.database import db

if __name__ == "__main__":
    app = create_app()

    migrate = Migrate(app, db)
    manager = Manager(app)

    manager.add_command("db", MigrateCommand)
    manager.run()
