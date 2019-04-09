import getpass
import unittest

from userconfiguration import UserConfiguration


class TestUserConfiguration(unittest.TestCase):
    self.username = 'hackathon@swimlaneresearchdev.onmicrosoft.com'
    self.password = getpass.getpass()

    def test_credentials_username(self):
        result = UserConfiguration(self.username, self.password)
        self.assertEqual(result.credentials.email_address, self.username)

    def test_credentials_password(self):
        result = UserConfiguration(self.username, self.password)
        self.assertEqual(result.credentials.password, self.password)


if __name__ == '__main__':
    unittest.main()
