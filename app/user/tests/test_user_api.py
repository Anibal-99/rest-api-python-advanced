"""Test for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create_user")


def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user us successful"""

        payload = {
            "email": "anibal@example.com",
            "password": "anibal1234",
            "name": "Test name",
        }

        response = self.client.post(CREATE_USER_URL, payload)

        # usuario se creo correctamente en la base de datos, con el estado 201
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertTrue(user.has_usable_password())
        # varifica la data enviada en la respuesta, y que no esta la password
        self.assertNotIn("password", response.data)

    def test_user_with_email_exists_errors(self):
        """test error return if user with email exists"""
        payload = {
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test name",
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is return if password less than 5 characters"""

        payload = {
            "email": "test@example.com",
            "password": "te",
            "name": "Test name",
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """
        con esta parte lo que hacemos es verificar que el
        usaurio que esta intentando registrarse con una password corta,
        tampoco se esta registrando en la db
        """
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )

        self.assertFalse(user_exists)
