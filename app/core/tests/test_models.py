"""Tests for models"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """test model"""

    def test_create_user_with_email_successfull(self):
        """test creating a user with an email is succefull"""

        email = "anit4@gmail.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)

    def test_new_user_email_normalized(self):
        """
        Test email is normalized for new users

        crea una serie de emails validos, luego se crea un usario
        con un email cualquiera y se lo compara con la lista de
        email esperados, para que pueda pasar el test
        """

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raised_error(self):
        """Test that creating a user without an email raised a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test1234")

    def test_create_superuser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test1234",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
