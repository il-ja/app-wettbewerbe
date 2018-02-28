from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from . import models

import ipdb

# Create your views here.

class IndexView(ListView):
    """ zeigt die Startseite an :) """
    def get_queryset(self):
        """ gibt dict mit Listen der Objekte zurück """
        return {
            'wettbewerbe': models.WettbewerbKonkret.objects.all(),
            'veranstaltungen': models.Veranstaltung.objects.all(),
        }

    template_name = 'Wettbewerbe/index.html'
    context_object_name = 'listen'

class ListeWettbewerbe(ListView):
    """ zeigt Liste der Wettbewerbe an :) """
    model = models.WettbewerbKonkret
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
    """ Gibt einen konkreten Wettbewerb zurück """
    def get_object(self, *args, **kwargs):
        wettbewerb = get_object_or_404(
            models.WettbewerbPrinzipiell,
            slug=self.kwargs['slug'],
            slug_prefix=self.kwargs['slug_prefix'],
        )
        return wettbewerb

    template_name = 'Wettbewerbe/ein_wettbewerb.html'
    context_object_name = 'wettbewerb'

class EinWettbewerbKonkret(EinWettbewerb):
    def get_object(self, *args, **kwargs):
        wettbewerb = super().get_object(*args, **kwargs)
        return get_object_or_404(
            wettbewerb.jahrgaenge,
            jahrgang=int(self.kwargs['jahrgang']),
        )


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

