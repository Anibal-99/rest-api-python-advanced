"""Test for recipe API"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse("recipe:recipe-list")


def create_user(**params):
    """created and return a new user"""
    return get_user_model().objects.create_user(**params)


def detail_url(recipe_id):
    """Create and return a recipe detail URL"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **params):
    """create and return a sample recipe"""

    defaults = {
        "title": "sample recipe title",
        "time_minutes": 5,
        "price": Decimal("5.25"),
        "description": "sample description",
        "link": "http://example.com/recipe.pdf",
    }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeApiTest(TestCase):
    """Test unauthenticated api request"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        response = self.client.get(RECIPES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test authenticated API request"""

    def setUp(self) -> None:
        """creo un cliente y luego autentico el cliente con el
        usuario que estoy creando"""
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com", password="testpass1234"
        )

        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Test retrieving a list off recipes."""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user"""
        other_user = create_user(
            email="other@example.com",
            password="testpass1234",
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail"""

        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        response = self.client.get(url)

        serializer = RecipeSerializer(recipe)

        self.assertEqual(response.data, serializer.data)

    def test_create_recipe(self):
        """test creating recipe"""

        payload = {
            "title": "sample recipe",
            "time_minutes": 30,
            "price": Decimal("5.99"),
        }

        response = self.client.post(RECIPES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data["id"])

        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # nos aseguramos de que la receta ya no existe en la db
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
