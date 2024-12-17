from django.urls import path

from viewer.views import MoviesView, MoviesDetail, ActorsView, ActorsDetail, MovieCreateView, home, MovieUpdateView, \
    MovieDeleteView

app_name = 'viewer'

urlpatterns = [
    path('', MoviesView.as_view(), name='movies'),

    # Observatie: Aveti grija la ordinea path-urilor
    # Ele sunt verificate in ordine de la primul la ultimul
    path('create', MovieCreateView.as_view(), name='movies_create'),
    path('update/<pk>', MovieUpdateView.as_view(), name='movies_update'),
    path('delete/<pk>', MovieDeleteView.as_view(), name='movies_delete'),

    path('<pk>', MoviesDetail.as_view(), name='movies_detail'),
]