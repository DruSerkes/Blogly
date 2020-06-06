from unittest import TestCase
from app import app
from models import db, User, Post

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
        Post.query.delete()

        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='Testing content...', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """ Clean up session """
        db.session.rollback()

    def test_home_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    # USER TESTS 

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

    # BLOG POST TESTS 
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)
            self.assertIn('Testing content', html)

    def test_add_post(self):
        with app.test_client() as client:
            post = {
                'title': 'Test Post2',
                'content': 'Testing content again',
                'user_id': self.user_id
            }
            resp = client.post(f'/users/{self.user_id}/posts/new', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post2', html)

    def test_edit_post(self):
        with app.test_client() as client:
            post = {
                'title': 'Test Edit Post',
                'content': 'Test edited content'
            }
            resp = client.post(
                f'/posts/{self.post_id}/edit', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Edit Post', html)
            self.assertIn('Test edited content', html)

    def test_delete_post(self):
        with app.test_client() as client:
            client.get(f'/posts/{self.post_id}')
            resp = client.post(
                f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test Post', html)
            self.assertNotIn('Test Edited Post', html)
