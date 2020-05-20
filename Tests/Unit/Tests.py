import coverage

BASEDIR = '/Volumes/SANDISK/Python Projects/DVDLibrary/application/'
cov = coverage.Coverage(source=[BASEDIR], branch=True, omit=['Tests.py'])
cov.start()

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
        response = self.register(name='Mark', email='mark@mgurney.co.uk', password='FlaskisAwesome',
                                 confirm='FlaskisAwesome', rules=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations on signing up to the Ben Rhydding DVD Lending Library', response.data)

    def test_login_form(self):
        u = User(name='Mark', email='mark@mgurney.co.uk', rules_read=True)
        u.set_password('imogen')
        db.session.add(u)
        db.session.commit()
        response = self.login('mark@mgurney.co.uk', 'imogen')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Invalid username/password combination', response.data)

    def test_unauthorised(self):
        response = self.app.get('/library')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Redirecting...', response.data)
        self.assertIn(b'/login', response.data)

    def test_dvd_lib(self):
        self.create_test_user()
        self.login_test_user()
        response = self.app.get('/library')
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/library', data=dict(dvd_select='Title', dvd_search='Lion'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Items', response.data)
        print(response.status_code, response.data)

    # ##########################
    # Helper functions for tests
    # ##########################

    def register(self, name, email, password, confirm, rules):
        return self.app.post(
            '/signup',
            data=dict(name=name, email=email, password=password, confirm=confirm, read_rules=rules),
            follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def create_test_user(self):
        return self.app.post('/signup',
                             data=dict(name='Mark', email='mark@mgurney.co.uk', password='imogen', confirm='imogen',
                                       read_rules=True))

    def login_test_user(self):
        return self.app.post('/login', data=dict(email='mark@mgurney.co.uk', password='imogen'))


if __name__ == "__main__":
    try:
        unittest.main()
    except:
        pass

cov.stop()
cov.save()
print("\n\nCoverage Report:\n")
cov.report()
cov.html_report(directory='tmp/coverage')
cov.erase()
