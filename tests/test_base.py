from flask_testing import TestCase
from flask import current_app, url_for

from main import app
from app.firestore_service import db

#flask test
class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        return app

    
    def test_app_exists(self):
        self.assertIsNotNone(current_app)
    
    
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        self.assertEqual(response.location, url_for('hello'))

    
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))

        self.assert200(response)

    
    def test_hello_post(self):
        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    
    def test_auth_blueprint_exist(self):
        self.assertIn('auth', self.app.blueprints)

    
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    
    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))

        self.assertTemplateUsed('login.html')


    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password',
        }

        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertEqual(response.location, url_for('index'))


    def test_auth_signup_get(self):
        response = self.client.get(url_for('auth.signup'))

        self.assert200(response)


    def test_auth_signup_template(self):
        self.client.get(url_for('auth.signup'))

        self.assertTemplateUsed('signup.html')


    def test_auth_signup_post(self):
        try:
            fake_form = {
                'username': 'test_user',
                'password': '123456'
            }
            response = self.client.post(url_for('auth.signup'), data=fake_form)
            self.assertEqual(response.location, url_for('hello'))
        finally:
            #Remove added db
            db.collection('users').document(fake_form['username']).delete()
