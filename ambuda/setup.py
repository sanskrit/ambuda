from ambuda import app, db
from ambuda.models import Status


@app.before_first_request
def create_status():
    """Create some basic `Status` objects."""
    if Status.query.count():
        return
    for name in ['proofreading-1', 'proofreading-2', 'formatting-1',
                 'formatting-2', 'complete']:
        db.session.add(Status(name=name))
    db.session.commit()
