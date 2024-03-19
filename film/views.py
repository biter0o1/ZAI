from .models import Film
from .serializers import FilmModelSerializer, UserSerializerShort, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User


class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class FilmRetrieve(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class FilmCreateList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerShort

class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer