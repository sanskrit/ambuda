from ambuda import create_app
from ambuda.models import *


def populate_db():
    db.create_all()


def main():
    app = create_app(__name__, 'development.config')
    with app.app_context():
        populate_db()
    print 'Done.'


if __name__ == '__main__':
    main()
