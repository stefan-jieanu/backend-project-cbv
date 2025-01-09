from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Genre, Movie, Actor
from django.utils.translation import gettext_lazy as _
from datetime import date

# Register your models here.
admin.site.register(Genre)
# admin.site.register(Movie)
admin.site.register(Actor)

class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("decade born")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "decade"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("80s", _("in the eighties")),
            ("90s", _("in the nineties")),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "80s":
            return queryset.filter(
                released__gte=date(1980, 1, 1),
                released__lte=date(1989, 12, 31),
            )
        if self.value() == "90s":
            return queryset.filter(
                released__gte=date(1990, 1, 1),
                released__lte=date(1999, 12, 31),
            )

class MovieAdmin(ModelAdmin):

    ###### Modificat pagina cu lista de obiecte #####
    # Decoratorul @staticmethod indica faptul ca metoda respectiva
    # este o metoda de clasa, nu de obiect
    # NU exista parametrul self la metodele statice
    @staticmethod
    def released_year(obj):
        return obj.released.year

    @staticmethod
    # modeladmin este o referinta la clasa de ModelAdmin (in cazul nostru va fi MovieAdmin)
    # request este request-ul de la client (asemanatorul cu cel dintr-un view)
    # queryset va fi obiectele selectate in pagina de admin
    def clean_description(modeladmin, request, queryset):
        queryset.update(description='')

    # Functille din actions vor aparea in sectiunea actions
    # din pagina de admin
    actions = ['clean_description']

    # Ordinea in care apar filmele in lista
    ordering = ['id']

    # Proprietatile unui model care apar in lista
    list_display = ['id', 'title', 'genre', 'released_year']

    # Proprietatile care apar ca si link la filmul respectiv
    list_display_links = ['id', 'title']

    # Numarul de filme care apar pe o pagina
    # exemplu: list_per_page = 2
    # prima pagina va contine primele 2 filme, urmatoarea inca 2, etc
    list_per_page = 10

    # Proprietati dupa care putem filtra rezultatele din pagina
    list_filter = ['title', 'released', 'genre', DecadeBornListFilter]

    # Adauga un input de cautat filme dupa un input de la utilizator
    search_fields = ['title']

    ###### Modificat pagina cu detaliile unui obiect #####
    # ('Nume sectiune', {'fields': ['nume field'], 'description': ('descriere sectiune')})
    fieldsets = [
        ('Detalii esentiale', {'fields': ['title', 'created']}),
        (
            'Alte detalii',
            {
                'fields': ['released', 'rating', 'description', 'actors'],
                # description poate fi un simplu string
                'description': 'ceva alte detalii'
            }
        ),
        (
            'Gen',
            {
                'fields': ['genre'],
                # sau description poate fi un tuple cu mai multe strings
                # (ca si functionalitate pe pagina sunt echivalente)
                'description': (
                    'Acesta este '
                    'desc film'
                )
            }
        )
    ]

    # created se adauga in mod automat pentru ca am specificat in model auto_now_add=True
    # si nu poate fi modificata (adica este 'readonly').
    # Toate field-urile din model care nu pot fi modificate si apar in pagina
    # trebuie specificate in acest readonly_fields
    readonly_fields = ['created']


admin.site.register(Movie, MovieAdmin)
