"""
URL configuration for hollymovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from viewer.views import MoviesView, MoviesDetail, ActorsView, ActorsDetail, MovieCreateView, home, MovieUpdateView, \
    MovieDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('movies/', MoviesView.as_view(), name='movies'),

    # Observatie: Aveti grija la ordinea path-urilor
    # Ele sunt verificate in ordine de la primul la ultimul
    path('movies/create', MovieCreateView.as_view(), name='movies_create'),
    path('movies/update/<pk>', MovieUpdateView.as_view(), name='movies_update'),
    path('movies/delete/<pk>', MovieDeleteView.as_view(), name='movies_delete'),

    path('movies/<pk>', MoviesDetail.as_view(), name='movies_detail'),

    path('actors/', ActorsView.as_view(), name='actors'),
    path('actors/<pk>', ActorsDetail.as_view(), name='actors_detail'),
]
