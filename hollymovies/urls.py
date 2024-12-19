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
from django.urls import path, include

from viewer.views import MoviesView, MoviesDetail, ActorsView, ActorsDetail, MovieCreateView, home, MovieUpdateView, \
    MovieDeleteView, ActorsCreateView

from viewer import urls as viewer_urls
from accounts import urls as accounts_urls

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts paths
    path('accounts/', include(accounts_urls, namespace='accounts')),

    path('', home, name='home'),

    path('movies/', include(viewer_urls, namespace='viewer')),

    path('actors/', ActorsView.as_view(), name='actors'),
    path('actors/create', ActorsCreateView.as_view(), name='actors_create'),
    path('actors/<pk>', ActorsDetail.as_view(), name='actors_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ^ adaugam linkuri pentru fisierele statice
