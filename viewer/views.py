from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from viewer.models import Movie, Actor
from viewer.forms import MovieForm, ActorForm

# Test custom pentru a verifica o conditie pentru a accesa un view
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Create your views here.
def home(request):
    # Functia redirect va redirectiona site-ul spre un alt link
    # Acel link poate fi de la alt site, sau un link de pe site-ul nostru
    # exemplu site extern: return redirect('https://google.com')

    # Acest view ne va redirectiona pe pagina de /movies
    return redirect('/movies')


# @login_required este echivalent cu LoginRequiredMixin la clase
# Dar se foloseste pentru views tip functie.
# @permission_required echivalent cu PermissionRequiredMixin la clase
# exemplu: @permission_require('viewer.view_movie')
@login_required
def pagina(request):
    return HttpResponse('pagina pentru utilizatori')

# class MoviesView(View):
#     def get(self, request):
#         return render(
#             request,
#             template_name='movies.html',
#             context={'movies_list': Movie.objects.all()}
#         )

# SAU folosind TemplateView
# class MoviesView(TemplateView):
#     template_name = 'movies.html'
#
#     # In clasele de tipul TemplateView
#     # extra_context are acelasi rol ca si context din
#     # functia de render()
#     extra_context = {'movies_list': Movie.objects.all()}

# SAU folosind ListView
class MoviesView(ListView):
    # Clasa ListView va defini automat un context={'object_list': Movie.objects.all()}
    template_name = 'movies.html'
    model = Movie

    # Permisiunea necesara pentru a accesa pagina
    # Structura permisiunii este: numeapp.numepermisiune_numemodel
    # permission_required = 'viewer.view_movie'


# DetailView este folosit pentru a luat un singur obiect din baza de date dupa pk (primary key)
class MoviesDetail(LoginRequiredMixin, DetailView):
    template_name = 'movies_detail.html'
    model = Movie


# StaffRequiredMixin va verifica conditia creata de noi mai sus
# anume, daca utilizatorul este staff sau nu
class ActorsView(StaffRequiredMixin, ListView):
    template_name = 'actors.html'
    model = Actor


class ActorsDetail(DetailView):
    template_name = 'actors_detail.html'
    model = Actor


class ActorsCreateView(CreateView):
    template_name = 'actors_form.html'
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy('actors')

    def form_invalid(self, form):
        print('User provided invalid data!')
        return super().form_invalid(form)

# FormView este o clasa pentru un formular generic
# In functia de form_valid noi putem face orice
# (salvat un obiect in baza de date, trimis un mail cu datele, etc)
# class MovieCreateView(FormView):
#     template_name = 'movie_form.html'
#     form_class = MovieForm
#
#     def form_valid(self, form):
#         # Luam resultate din formular folosind functia de baza din FormView
#         result = super().form_valid(form)
#         cleaned_data = form.cleaned_data
#
#         Movie.objects.create(
#             title = cleaned_data['title'],
#             genre = cleaned_data['genre'],
#             rating = cleaned_data['rating'],
#             released = cleaned_data['released'],
#             description = cleaned_data['description']
#         )
#
#         return result
#
#     # success_url este link-ul la care vom fi trimisi dupa completarea formularului
#     # functia reverse_lazy() na va return un path definiti in urls.py dupa nume
#     success_url = reverse_lazy('movies')

class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'movie_form.html'
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movies')

    permission_required = 'viewer.add_movie'

    # Functie care se apeleaza automat daca formularul este invalid
    def form_invalid(self, form):
        print('User provided invalid data!')
        # Trebuie sa scriem acest return ca sa respectam logica originala a functiei
        return super().form_invalid(form)


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'movie_form.html'
    form_class = MovieForm
    model = Movie
    success_url = reverse_lazy('viewer:movies')

    permission_required = 'viewer.change_movie'


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('viewer:movies')
    permission_required = 'viewer.delete_movie'


