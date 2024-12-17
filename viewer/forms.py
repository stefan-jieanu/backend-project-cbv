import re
from datetime import date

from django.db.models.expressions import result
from django.forms import *

from viewer.models import Genre, Movie, Actor


# Clasa creata de noi pentru a afisa in formular un widget
# cu HTML-ul necesar pentru un calendar
class DateInput(DateInput):
    input_type = 'date'

# clasa Form se foloseste pentru a crea un formular generic
# adica il folosim noi in ce scop vrem
# class MovieForm(Form):
#     title = CharField(max_length=128)
#     rating = IntegerField(min_value=1, max_value=10)
#
#     # widget indica ca in HTML tag-ul pentru field-ul acesta
#     # ar trebui sa fie un textarea
#     description = CharField(widget=Textarea)
#
#     # ModelChoiceField o sa genereze un dropdown
#     # in care optiunile sunt modelul specificat in queryset
#     genre = ModelChoiceField(queryset=Genre.objects)
#
#     released = DateField(widget=DateInput)

def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('First letter must be capitalized.')


class PastDateField(DateField):
    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Movie cannot be from future.')


class MovieForm(ModelForm):
    # Speficifam detalii pentru formular
    class Meta:
        # Indicam modelul folosit
        model = Movie

        # Indicam ce field-uri din model sa folosim
        # '__all__' o sa le includa pe toate
        fields = '__all__'
        # SAU
        # Daca vrem sa specificam fieldurile
        # fields = ['title', 'description']
        # SAU
        # Daca vrem sa includem toate filedurile cu cateva exceptii
        # De exemplu ca sa excludem field-ul 'released'
        # exclude = ['released']

    # Suprascriem constructorul formularului
    # Acest constructor ruleza cand se genereaza formularul
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Returneza o lista cu toate field-urile vizibile din formular
        v_fields = self.visible_fields()

        for field in v_fields:
            # Accesam attributes din interiorul tag-ului <input >
            # care a fost generat pentru fiecare field
            # si ii adaugam attr-ul de class='form-control'
            field.field.widget.attrs['class'] = 'form-control'


    title = CharField(max_length=128, validators=[capitalized_validator])
    released = PastDateField(widget=DateInput)
    rating = IntegerField(min_value=1, max_value=10)

    def clean_description(self):
        # Force each first letter of sentence to be capitalized

        # Initial value of field description
        initial = self.cleaned_data['description']

        # Split description in a list of sentence
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')

        # Join all sentences in a single text
        final = '. '.join(sentence.capitalize() for sentence in sentences)
        return final

    def clean(self):
        result = super().clean()

        if result['genre'].name == 'Comedie' and result['rating'] < 5:
            # Functia self.add_error('fieldname', 'message') va adauga o eroare pentru un singur field
            # fieldname este numele field-ului unde va aparea eroarea
            # message este mesajul erorii
            self.add_error('genre', 'Atentie field genre.')
            self.add_error('rating', 'Atentie field rating')
            raise ValidationError('Comedy movies must be above 5.')

        return result

class ActorForm(ModelForm):
    class Meta:
        model = Actor
        fields = '__all__'

    date_of_birth = DateField(widget=DateInput)