from django.conf.urls import url, include
from . import views

app_name = 'Wettbewerbe'

# Hilfspatterns gruppiert
wettbewerbe_urls = [
    url(r'^(?P<slug_prefix>[\w-]+)/(?P<jahrgang>[1-9]+)/(?P<slug>[\w-]+)$',
        views.EinWettbewerbKonkret.as_view(),
        name='ein_wettbewerb_konkret',
    ),
    url(r'^(?P<slug_prefix>[\w-]+)/(?P<slug>[\w-]+)$',
        views.EinWettbewerb.as_view(),
        name='ein_wettbewerb_generisch',
    ),
]

# Die unmittelbar genutzten url-patterns
urlpatterns = [
    # Übersichtsseiten:
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^wettbewerbe/$',
        views.ListeWettbewerbe.as_view(),
        name='liste_wettbewerbe',
    ),
    url(r'^veranstaltungen/$',
        views.ListeVeranstaltungen.as_view(),
        name='liste_veranstaltungen',
    ),
    url(r'^personen/$',
        views.ListePersonen.as_view(),
        name='liste_personen',
    ),
    # Detailseiten:
    url(r'^wettbewerb/', include(wettbewerbe_urls)),
    url(r'^veranstaltung/(?P<slug>[\w-]+)/$',
        views.EineVeranstaltung.as_view(),
        name='eine_veranstaltung',
    ),
    url(r'^person/(?P<pk>[\w-]+)/$',
        views.EinePerson.as_view(),
        name='eine_person',
    ),
    # Formulare:
    url(r'^wettbewerb/(?P<slug>[\w-]+)/mich_eintragen/$',
        views.EintragenInWettbewerb.as_view(),
        name='mich_eintragen_wettbewerb',
    ),
    url(r'^veranstaltung/(?P<slug>[\w-]+)/mich_eintragen/$',
        views.EintragenInVeranstaltung.as_view(),
        name='mich_eintragen_veranstaltung',
    ),
]

