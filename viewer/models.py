from django.db import models
from django.db.models import *

# Create your models here.
class Genre(models.Model):

    # class Meta este o clasa creata in interiorul modelului
    # contine proprietati ale modelului care pot fi schimbate
    class Meta:
        # attributul 'verbose_name_plural' este numele care va aparea pe pagina de admin
        # exemplu:
        verbose_name_plural = 'Genuri de filme'

    # Field in modelul Genre numit 'name' care este de tip CharField (mai exact, un string)
    # max_length este un parametru care indica lungimea maxima al acestui field
    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = CharField(max_length=128)
    description = TextField()
    date_of_birth = DateField()

    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):

    class Meta:
        verbose_name_plural = 'Filme'

    title = CharField(max_length=128)

    # IntegerField este un field care simbolizeaza un simplu int
    rating = IntegerField()

    # DateField este un field in care o sa se salveze un obiect Date care include zi, luna, an
    released = DateField()

    # TextField va contine un simplu string, indiferent de lungimea lui
    description = TextField()

    # ForeignKey face referire la un alt tabel din baza de date
    # on_delete insemna ce actiune se va intempla cand randul la care facem referire este sters
    # DO_NOTHING inseamna ca nu se va intampla nimic
    genre = ForeignKey(Genre, on_delete=DO_NOTHING)

    # DateTimeField este un field care va contine zi, luna, an, ora, minut
    # auto_now_add specifica daca sa va completa campul automat cand este salvat obiectul
    created = DateTimeField(auto_now_add=True)

    # ManyToMany insemna ca un film poate avea mai multi actori
    # si un actor poate fi parte din mai multe filme
    actors = ManyToManyField(Actor)

    def __str__(self):
        return f'Titlul filmului este: {self.title}'


