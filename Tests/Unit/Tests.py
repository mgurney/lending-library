BASEDIR = '/Volumes/SANDISK/Python Projects/DVDLibrary/application/'
# cov = coverage.Coverage(source=[BASEDIR], branch=True, omit=['Tests.py'])
# cov.start()

import unittest

from application import db
from application.models import User
from wsgi import app


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUB'] = True

        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    ###############
    #### tests ####
    ##############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_signup_function(self):
        response = self.register('Mark', 'mark@mgurney.co.uk', 'FlaskisAwesome', 'FlaskisAwesome', 'True')
        print(response.data)
        user = User.query.filter_by(email='mark@mgurney.co.uk')
        #        print(user)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='mark@mgurney.co.uk').first()

    #        print(user)

    def test_login_form(self):
        u = User(name='Mark', email='mark@mgurney.co.uk', password='imogen', rules_read=True)
        db.session.add(u)
        db.session.commit()
        #        user = User.query.filter_by(email='mark@mgurney.co.uk')
        #        print(user)
        response = self.login('mark@mgurney.co.uk', 'imogen')
        self.assertEqual(response.status_code, 200)
        #        print(response.data)
        self.assertNotIn(b'Invalid username/password combination', response.data)

    # Helper functions for tests

    def register(self, name, email, password, confirm, rules):
        return self.app.post(
            '/signup',
            data=dict(name=name, email=email, password=password, confirm=confirm, rules=rules),
            follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)


if __name__ == "__main__":
    try:
        unittest.main()
    except:
        pass

# cov.stop()
# cov.save()
# print("\n\nCoverage Report:\n")
# cov.report()
# cov.html_report(directory='tmp/coverage')
#cov.erase()
