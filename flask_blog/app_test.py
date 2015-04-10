import os
import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.db_fd,app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()
        
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
        
    def login(self,username,password):
        return self.app.post('/login',data = dict(username=username,password=password),follow_redirects = True)
        
    def logout(self):
        return self.app.get('/logout',follow_redirects=True)
        
    def test_login_logout(self):
        rv = self.login('admin','default')
        assert 'You are logged in' in rv.data
        rv = self.logout()
        assert 'You are logged out' in rv.data
        rv = self.login('admin','defaultx')
        assert 'Password Invalid' in rv.data
        rv = self.login('adminx','defaultx')
        assert 'Username Invalid' in rv.data
        
    def test_messages(self):
        self.login('admin','default')
        rv = self.app.post('/add',data=dict(
            title='<Hello>',
            text = '<strong>Html</strong>allowed here'
        ),follow_redirects=True)
        assert 'No entries here so far' in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>Html</strong>allowed here' in rv.data
    
    def test_empty_db(self):
        rv = self.app.get('/')
        assert "No entries here so far" in rv.data

if __name__ == "__main__":
    unittest.main()