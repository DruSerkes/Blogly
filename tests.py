from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    def setUp(self):
        """Add sample user"""
        self.client = app.test_client()

        User.query.delete()

        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up session """
        db.session.rollback()

    def test_home_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)
            self.assertIn('Edit', html)

    def test_add_user(self):
        with app.test_client() as client:
            user = {
                'first-name': 'Test',
                'last-name': 'User2'
            }
            resp = client.post(f'users/new', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User2', html)

    def test_edit_user(self):
        with app.test_client() as client:
            user = {
                'first-name': 'Test',
                'last-name': 'User-Edit'
            }
            resp = client.post(
                f'users/{self.user_id}/edit', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User-Edit', html)

    def test_delete_user(self):
        with app.test_client() as client:
            client.get(f'/users/{self.user_id}')
            resp = client.post(
                f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test User', html)
