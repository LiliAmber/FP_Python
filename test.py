import unittest

import app
from directors import read_all, read_one
from movies import read_all, read_one

class TestCaseUrl(unittest.TestCase):
    def setUp(self):
        app.connex_app.app.testing = True
        self.app = app.connex_app.app.test_client()

    def test_get_all_directors(self):
        """
        This function expecting to a response of status code for /api/directors with code 200
        """
        result = self.app.get('/api/directors')
        self.assertEqual(result.status_code, 200)
    
    def test_get_all_movies(self):
        """
        This function expecting to a response of status code for /api/movies with code 200
        """
        result = self.app.get('api/movies')
        self.assertEqual(result.status_code, 200)

class TestDirectors(unittest.TestCase):
    def test_read_all(self):
        """
        This function expecting to a response for /api/directors with list data type
        """
        self.assertIs(type(read_all()), list)

    def test_read_all_err(self):
        """
        This function expecting to a response for /api/directors not in dictionary data type
        """
        self.assertIsNot(type(read_all()), dict)

    # def test_read_one(self):
    #     self.assertIs(type(read_one(director_id=43597)), dict)

class TestMovies(unittest.TestCase):
    def test_read_all(self):
        """
        This function expecting to a response for /api/movies with list data type
        """
        self.assertIs(type(read_all()), list)

    def test_read_one(self):
        """
        This function expecting to a response for /api/movies/{movie_id} with dictionary data type
        """
        self.assertIs(type(read_one(movie_id=43597)), dict)

if __name__ == '__main__':
    unittest.main()