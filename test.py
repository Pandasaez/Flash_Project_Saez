import unittest
import warnings
from api import app

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        
        warnings.simplefilter("ignore", category=DeprecationWarning)
        
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello Testing</p>")
        
    def test_getstudent(self):
        response = self.app.get("/information")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jasper" in response.data.decode())
        
        
    def test_getstudent_by_ID(self):
        response = self.app.get("/information/student/1234")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jiro" in response.data.decode())
        
if __name__ == "__main__":
    unittest.main()