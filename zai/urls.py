"""
URL configuration for zai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import wszystkie, szczegoly, nowy, edycja, usun
from film.views import FilmList, FilmRetrieve, FilmCreateList, UserList, UserCreateList

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('filmlist/', FilmList.as_view(), name='FilmList'),
    path('filmretrieve/<int:pk>/', FilmRetrieve.as_view(), name='FilmRetrieve'),
    path('filmcreatelist/', FilmCreateList.as_view(), name='FilmCreateList'),
    path('userlist/', UserList.as_view(), name='UserList'),
    path('usercreatelist/', UserCreateList.as_view(), name='UserCreateList'),


    path('wszystkie/', wszystkie),
    path('szczegoly/<int:film_id>/', szczegoly),
    path('nowy/', nowy),
    path('edycja/<int:film_id>/', edycja),
    path('usun/<int:film_id>/', usun)
]
