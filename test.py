import unittest

from directors import read_all, read_one
from movies import read_all, read_one


class TestDirectors(unittest.TestCase):

    def test_read_all(self):
        self.assertIs(type(read_all()), list)

    def test_read_all_err(self):
        self.assertIsNot(type(read_all()), dict)
    
    # def test_read_one(self):
    #     self.assertIs(type(read_one(director_id=43597)), dict)

class TestMovies(unittest.TestCase):
    def test_read_all(self):
        self.assertIs(type(read_all()), list)

    def test_read_one(self):
        self.assertIs(type(read_one(movie_id=43597)), dict)

if __name__ == '__main__':
    unittest.main()
