import unittest

from src.db import connect


class TestDatabaseConnection(unittest.TestCase):
    def test_connect(self):
        conn = connect()
        self.assertIsNotNone(conn)


if __name__ == "__main__":
    unittest.main()
