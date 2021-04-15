from django.shortcuts import render
from movies.models import *
from django.views.generic import DetailView, ListView


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
    context_object_name = 'film_detail' # Jméno kontextu
    template_name = 'film/detail.html' # Složka, kam se údaj o filmu vypíše


# Předem připravený instantní pohled, který můžeme využívat v rámci výpisů
# Předek ListView vypíše více popložek
class FilmListView(ListView):
    model = Film

    context_object_name = 'film_list' # Jméno kontextu, proměnná, která se vyobrazuje na list.html
    template_name = 'film/list.html' # Složka, kam se údaj o filmu vypíše, šablona
    paginate_by = 4

def topten(request):
    return render(request, 'topten.html')
