from rest_framework import serializers
from main.models import Film
from django.contrib.auth.models import User

class FilmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "is_superuser", "email", "is_staff", "is_active"]