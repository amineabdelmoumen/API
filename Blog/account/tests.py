
from rest_framework.test import force_authenticate
import json
from .models import User, Book, Profil
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from account.serializers import UserSerializer, BookSerializer, ProfilSerializer


class RegisterNewUserTestCase(APITestCase):
    def test_registration(self):
        register = reverse('register')
        data = {"email": "abamine22@gmail.com", "username": "Tajani",
                "password": "Djan@2020", "password1": "Djan@2020"}
        response = self.client.post(register, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class getusersandtheirBooksTestCase(APITestCase):

    def test_authenticated_user(self):
        request_reverse = reverse("users_all_inf")
        user = User.objects.create(
            username='Tajani', password="StrongPassword")
        self.client.force_authenticate(user=user)
        response = self.client.get(request_reverse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthentication_user(self):
        request_reverse = reverse("users_all_inf")
        self.client.force_authenticate(user=None)
        response = self.client.get(request_reverse)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
