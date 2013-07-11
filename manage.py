from flask.ext.script import Manager
import flask.ext.security.script as sec
from ambuda import app

manager = Manager(app)
manager.add_command('create_user', sec.CreateUserCommand())
manager.add_command('create_role', sec.CreateRoleCommand())
manager.add_command('add_role', sec.AddRoleCommand())
manager.add_command('remove_role', sec.RemoveRoleCommand())


def main():
    manager.run()


if __name__ == '__main__':
    main()
