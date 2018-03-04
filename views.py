from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return self.model.objekt_aus_kwargs(self.kwargs)

    model = models.WettbewerbPrinzipiell
    template_name = 'Wettbewerbe/ein_wettbewerb.html'
    context_object_name = 'wettbewerb'

class EinWettbewerbKonkret(EinWettbewerb):
    model = models.WettbewerbKonkret

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

class EintragenInEvent(LoginRequiredMixin, CreateView):
    """ zum Eintragen des Nutzers in Veranstaltung oder Wettbewerb

    Leitet zum login weiter, falls man nicht angemeldet ist.
    Öffnet Formular, in dem man die Art der Teilnahme wählen kann. """
    login_url = '/login/'
    fields = ['art']

    def objekt_suchen(self):
        pass

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission() # aus LoginRequiredMixin
        nutzer = self.request.user
        if not hasattr(nutzer, 'person'):
            self.person = models.Person.erstellen(nutzer)
        else:
            self.person = nutzer.person
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """ kwargs für die Initialisiegung der form zurückgeben

        erstellt eine Teilnahme und übergibt sie als instance-Argument
        dem Formular zusätzlich zu sonst übergebenen kwargs, sodass
        die form gleich bei erstellung bound ist. """
        kwargs = super().get_form_kwargs()
        objekt = self.objekt_suchen()
        person = self.person
        instanz = self.model.erstellen(
            person=person,
            objekt=objekt,
        )
        kwargs.update([('instance', instanz)])
        return kwargs

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['art'].queryset = \
            form.instance.erlaubte_arten()
        return form


class EintragenInVeranstaltung(EintragenInEvent):
    """ spam-implementierung """
    model = models.Teilnahme
    template_name = 'Wettbewerbe/formular_teilnahme_micheintragen.html'

    def objekt_suchen(self):
        return get_object_or_404(
            models.Veranstaltung,
            slug=self.kwargs['slug'],
        )

    def get_success_url(self):
        return reverse(
            'Wettbewerbe:eine_veranstaltung',
            kwargs={'slug': self.kwargs['slug']}
        )

class EintragenInWettbewerb(EintragenInEvent):
    """ spam-implementierung """
    model = models.Erfolg
    template_name = 'Wettbewerbe/formular_teilnahme_micheintragen.html'

    def objekt_suchen(self):
        return models.WettbewerbKonkret.objekt_aus_kwargs(self.kwargs)

    def get_success_url(self):
        return self.objekt_suchen().get_absolute_url()

