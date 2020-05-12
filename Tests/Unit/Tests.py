import coverage

BASEDIR = '/Volumes/SANDISK/Python Projects/DVDLibrary/application/'
cov = coverage.Coverage(source=[BASEDIR], branch=True, omit=['Tests.py'])
cov.erase()
cov.start()

import unittest
from wsgi import app
from application import db
import os
from application.models import User


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

        response = self.register('Pat Kennedy', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', False)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        u = User(name='Mark', email='mark@mgurney.co.uk', password='imogen', rules_read=True)
        db.session.add(u)
        db.session.commit()
        response = self.login('mark@mgurney.co.uk', 'imogen')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Invalid username/password combination', response.data)

    # ###########################
    #
    # Helper functions for tests
    #
    # ############################
    def register(self, name, email, password, confirm, rules):
        return self.client.post(
            '/signup',
            data=dict(name=name, email=email, password=password, confirm=confirm, rules=rules),
            follow_redirects=False)

    def login(self, email, password):
        return self.client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


if __name__ == "__main__":
    try:
        unittest.main()
    except:
        pass

cov.stop()
cov.save()
print("\n\nCoverage Report:\n")
cov.report()
print("HTML version: " + os.path.join(BASEDIR, "tmp/coverage/index.html"))
cov.html_report(directory='tmp/coverage')
cov.erase()
