#services/users/manage.py
import sys
import os
import unittest
import coverage

from flask import jsonify
from flask.cli import FlaskGroup

from project import create_app ,db
from project.models import User


COV = coverage.coverage(
    branch = True,include = 'project/*',
    omit = [
        'project/tests/*','project/config.py'
    ]
)

COV.start()


app = create_app(os.getenv('FLASK_CONFIG') or "default")

cli = FlaskGroup(app)


@app.cli.command()
def recreate_db():
    """Rebuild the databases NB:This will destroy any data currently in the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("%s has been recreated." %db)

@app.cli.command()
def cov():
    """Run the tests with code-coverage"""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

@app.cli.command()
def seed_db():
    """Add test users to the database"""
    db.session.add(User(username="fortie",name="Fort Power",email="fortie@swiftmail.com"))
    db.session.add(User(username="pot pot",name="Pot Pot",email="potpot@swiftmail.com"))
    db.session.commit()

@app.cli.command()
def test():
    """Run the tests without code-coverage"""
    tests = unittest.TestLoader().discover("project/tests",pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@app.shell_context_processor
def shell_context_processor():
    return dict(User=User,db=db)

if __name__=="__main__":
    cli()