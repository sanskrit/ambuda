from ambuda import db
from ambuda.models import *


def main():
    db.create_all()

    if not Flag.query.count():
        print 'Creating flags...'
        names = ['submit', 'complete', 'hard', 'pass']
        for name in names:
            db.session.add(Flag(name=name))

    if not Status.query.count():
        print 'Creating statuses...'
        names = ['incomplete', 'complete', 'verified']
        for name in names:
            db.session.add(Status(name=name))

    print 'Done.'
    db.session.commit()


if __name__ == '__main__':
    main()
