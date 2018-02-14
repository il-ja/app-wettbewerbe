from django.views.generic import ListView, DetailView, CreateView
from . import models

# Create your views here.

class IndexView(ListView):
    """ zeigt die Startseite an :) """
    def get_queryset(self):
        """ gibt dict mit Listen der Objekte zurück """
        return {
            'wettbewerbe': models.Wettbewerb.objects.all(),
            'veranstaltungen': models.Veranstaltung.objects.all(),
        }

    template_name = 'Wettbewerbe/index.html'
    context_object_name = 'listen'

class ListeWettbewerbe(ListView):
    """ zeigt Liste der Wettbewerbe an :) """
    model = models.Wettbewerb
    template_name = 'Wettbewerbe/liste_wettbewerbe.html'
    context_object_name = 'wettbewerbe'

class ListeVeranstaltungen(ListView):
    """ zeigt Liste der Veranstaltungen an :) """
    model = models.Veranstaltung
    template_name = 'Wettbewerbe/liste_veranstaltungen.html'
    context_object_name = 'veranstaltungen'

class ListePersonen(ListView):
    """ zeigt Liste der Personen an :) """
    model = models.Person
    template_name = 'Wettbewerbe/liste_personen.html'
    context_object_name = 'personen'

class EinWettbewerb(DetailView):
    """ spam-implementierung """
    model = models.Wettbewerb
    template_name = 'Wettbewerbe/ein_wettbewerb.html'
    context_object_name = 'wettbewerb'

class EineVeranstaltung(DetailView):
    """ spam-implementierung """
    model = models.Veranstaltung
    template_name = 'Wettbewerbe/eine_veranstaltung.html'
    context_object_name = 'veranstaltung'

class EinePerson(DetailView):
    """ spam-implementierung """
    model = models.Person
    template_name = 'Wettbewerbe/eine_person.html'
    context_object_name = 'person'

class EintragenInVeranstaltung(CreateView):
    """ spam-implementierung """
    model = models.Teilnahme
    template_name = 'Wettbewerbe/eine_veranstaltung.html'
    context_object_name = 'veranstaltung'

class EintragenInWettbewerb(CreateView):
    """ spam-implementierung """
    model = models.Erfolg
    template_name = 'Wettbewerbe/eine_veranstaltung.html'
    context_object_name = 'veranstaltung'

