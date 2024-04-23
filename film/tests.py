from django.contrib.auth import authenticate
from django.urls import path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.contrib.auth.models import User
from .views import FilmCreateList, FilmRetrieveUpdateDestroy, ExtraInfoCreateList, UserCreateList, UserRetrieveUpdateDestroy, statRezyserLiczbaFilmow
from .models import Film
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


LOGIN = 'admin'
PASSWORD = 'admin'

class TestyURL(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('filmy/', FilmCreateList.as_view(), name= 'FilmCreateList'),
        path('filmy/<int:pk>/', FilmRetrieveUpdateDestroy.as_view(), name='FilmRetrieveUpdateDestroy'),
        path('extrainfo/', ExtraInfoCreateList.as_view(), name='InformacjeDodatkowe'),
        path('user/', UserCreateList.as_view(), name='ListaUzytkownikow'),
        path('user/<pk>/', UserRetrieveUpdateDestroy.as_view(), name='UserRetrieveUpdateDestroy'),
        path('statRezyserLiczbaFilmow/', statRezyserLiczbaFilmow.as_view(), name='statRezyserLiczbaFilmow'),
    ]

    def setUp(self):
        admin = User.objects.create_superuser(username=LOGIN, password=PASSWORD)
        self.client.force_login(admin)


    def test_FilmCreateList(self):
        url = reverse('FilmCreateList')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmRetrieveUpdateDestroy(self):
        url = reverse('FilmRetrieveUpdateDestroy',args=[1])
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ExtraInfoCreateList(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        url = reverse('InformacjeDodatkowe')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ListaUzytkownikow(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        url = reverse('ListaUzytkownikow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UserRetrieveUpdateDestroy(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        url = reverse('UserRetrieveUpdateDestroy', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statRezyserLiczbaFilmow(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class Testy_Widokow(APITestCase):

    def setUp(self):
        User.objects.create_superuser(username=LOGIN, password=PASSWORD)

    def test_FilmCreateList_List(self):
        url = reverse('FilmCreateList')
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmCreateList_Create(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        url = reverse('FilmCreateList')
        film = {'tytul': 'Film testowy', 'rok': 2024, 'opis': 'opis'}
        response = self.client.post(url, film, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().rok, 2024)
        self.assertEqual(Film.objects.get().opis, 'opis')

    def test_FilmRetrieveUpdateDestroy_Retrieve(self):
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        url = reverse('FilmRetrieveUpdateDestroy', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')

    def test_FilmRetrieveUpdateDestroy_Update(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        Film.objects.create(tytul="Film testowy 2", rok=2024, opis="opis", owner=User.objects.get(id=1))
        url = reverse('FilmRetrieveUpdateDestroy', args=[1])
        film = {'tytul': 'Film testowy', 'rok': 2020, 'opis': 'opis opis'}
        response = self.client.put(url, film, format='json',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().rok, 2020)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().opis, 'opis opis')

    def test_FilmRetrieveUpdateDestroy_Destroy(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis", owner=User.objects.get(id=1))
        url = reverse('FilmRetrieveUpdateDestroy', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Film.objects.count(), 0)

    def test_statRezyserLiczbaFilmow(self):
        self.client.login(username=LOGIN, password=PASSWORD)
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)