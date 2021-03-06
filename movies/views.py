from django.shortcuts import render
from django.urls import reverse_lazy

from movies.forms import FilmModelForm
from movies.models import *
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView


# Create your views (pohledy) here.

# Pohledová metoda
def index(request):
    """Metoda připravuje pohled pro domovskou stránku - šablona index.html"""

    # Uložení celkového počtu filmů v databázi do proměnné num_films
    num_films = Film.objects.all().count()

    # Do proměnné films se uloží 3 filmy uspořádané podle hodnocení (sestupně), prvni 3 - od nulteho do tretiho
    films = Film.objects.order_by('-rate')[:3]

    """ Do proměnné context, která je typu slovník (dictionary) uložíme hodnoty obou proměnných """
    context = {
        'num_films': num_films,
        'films': films
    }

    """ Pomocí metody render vyrendrujeme šablonu index.html a předáme ji hodnoty v proměnné context k zobrazení """
    return render(request, 'index.html', context=context)


# Předem připravený instantní pohled, který můžeme již předem využít
# Předek DetailView vypíše pouze 1 položku
class FilmDetailView(DetailView):
    model = Film
    num_films = Film.objects.all().count()
    context_object_name = 'film_detail'  # Jméno kontextu
    template_name = 'film/detail.html'  # Složka, kam se údaj o filmu vypíše


# Předem připravený instantní pohled, který můžeme využívat v rámci výpisů
# Předek ListView vypíše více popložek
class FilmListView(ListView):
    model = Film

    context_object_name = 'film_list'  # Jméno kontextu, proměnná, která se vyobrazuje na list.html
    template_name = 'film/list.html'  # Složka, kam se údaj o filmu vypíše, šablona
    paginate_by = 4

    def get_queryset(self):
        # kwargs je klíčový argument, který pojmenuji 'genre_name'
        if 'genre_name' in self.kwargs:
            return Film.objects.filter(
                genres__name=self.kwargs['genre_name']).all()  # Get 5 books containing the title war
        else:
            return Film.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_films'] = len(self.get_queryset())
        if 'genre_name' in self.kwargs:
            context['view_title'] = f"Žánr: {self.kwargs['genre_name']}"
            context['view_head'] = f"Žánr filmu: {self.kwargs['genre_name']}"
        else:
            context['view_title'] = 'Filmy'
            context['view_head'] = 'Přehled filmů'
        return context


def topten(request):
    return render(request, 'topten.html')


# CreateView - instantní generický pohled
class FilmCreateView(CreateView):
    model = Film
    # Pole, která chceme, aby se nám zobrazovala
    fields = ['title', 'plot', 'poster', 'genres', 'release_date', 'runtime', 'rate']


class FilmUpdateView(UpdateView):
    model = Film
    # Vybere všechna políčka, avšak je zde potenciální bezpečnostní riziko
    # fields = '__all__' # Magická metoda, magický atribut
    form_class = FilmModelForm
    template_name = 'movies/film_bootstrap_form.html'


class FilmDeleteView(DeleteView):
    model = Film
    # Přesměrování stránky z důvodu toho, že záznam je vymazaný a nemáme se na něj jak dostat
    # Metoda reverse_lazy spolupracuje s urls.py, takže předáme, na jakou stránku nás to přesměruje - podle jména
    success_url = reverse_lazy('film_list')

