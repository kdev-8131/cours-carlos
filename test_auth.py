import tempfile
import unittest
from pathlib import Path

from auth import authenticate_user, register_user


class AuthenticationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.storage = Path(self.temporary_directory.name) / "users.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_register_and_login(self) -> None:
        self.assertTrue(register_user("carlos", "secret123", self.storage))
        self.assertTrue(authenticate_user("carlos", "secret123", self.storage))

    def test_wrong_password_is_rejected(self) -> None:
        register_user("carlos", "secret123", self.storage)
        self.assertFalse(authenticate_user("carlos", "incorrect9", self.storage))

    def test_duplicate_username_is_rejected(self) -> None:
        self.assertTrue(register_user("carlos", "secret123", self.storage))
        self.assertFalse(register_user("CARLOS", "another456", self.storage))

    def test_invalid_password_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            register_user("carlos", "court", self.storage)


if __name__ == "__main__":
    unittest.main()
