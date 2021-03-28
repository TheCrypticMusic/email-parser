import unittest
from main import EmailParser


class TestFileOpening(unittest.TestCase):

    def setUp(self):
        self.email = EmailParser()

    def test_file_validation(self):
        with self.assertRaises(ValueError):
            self.email.open_file("test.emt")
        with self.assertRaises(ValueError):
            self.email.open_file("test.email")
        self.assertTrue(type(self.email.open_file() is list))


class TestParsingEmail(unittest.TestCase):

    def setUp(self):
        self.email = EmailParser()

    def test_find_to_header(self):
        self.assertTrue("To:" in self.email.email)
        self.assertIn("@", self.email.email["To:"])
        self.assertGreater(len(self.email.email["To:"]), 0)
        self.assertTrue("<>" not in self.email.email["To:"])

    def test_find_from_header(self):
        self.assertTrue("From:" in self.email.email)
        self.assertIn("@", self.email.email["From:"])
        self.assertGreater(len(self.email.email["From:"]), 0)
        self.assertTrue("<>" not in self.email.email["From:"])

    def test_find_subject_header(self):
        self.assertTrue("Subject:" in self.email.email)
        self.assertGreater(len(self.email.email["Subject:"]), 0)


class TestResettingEmailContent(unittest.TestCase):

    def setUp(self):
        self.email = EmailParser()
        self.email.reset_values()

    def test_reset_values(self):
        self.assertTrue(self.email.email["To:"] == "")
        self.assertTrue(self.email.email["From:"] == "")
        self.assertTrue(self.email.email["Subject:"] == "")
        self.assertTrue(self.email.email["Content:"] == "")


class TestReturningEmailHeaders(unittest.TestCase):

    def setUp(self):
        self.email = EmailParser()

    def test_to_header(self):
        self.assertTrue(self.email.email_to)