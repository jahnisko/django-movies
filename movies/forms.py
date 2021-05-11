from django.core.exceptions import ValidationError
from django.forms import ModelForm
# from django.forms import Form
from .models import Film


class FilmModelForm(ModelForm):
    def clean_runtime(self):
        # self je v tomto případě náš formulář
        data = self.cleaned_data['runtime']
        if data <= 0 or data > 1000:
            # Volání výjimky
            raise ValidationError('Neplatná délka filmu')
        return data

    def clean_rate(self):
        data = self.cleaned_data['rate']
        if data < 1 or data > 10:
            # Volání výjimky
            raise ValidationError('Neplatné hodnocení: musí být v rozsahu 1-10')
        return data

    # Specifikuje některé parametry objektu
    class Meta:
        model = Film
        # Nedoporučuje se z důvodu nedostatečné bezpečnosti
        # fields = '__all__'
        fields = ['title', 'plot', 'poster', 'genres', 'release_date', 'runtime', 'rate']
        labels = {'title': 'Název filmu', 'plot': 'Stručný děj'}

