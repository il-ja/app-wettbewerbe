from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

from django.db import models
from Grundgeruest.models import Grundklasse, MinimalModel


""" Es werden folgende models definiert:
 - Person
 - Veranstaltung
 - Wettbewerb
 - Teilnahme, Erfolg
 - ArtTeilnahme, ArtErfolg, ArtVeranstaltung, ArtWettbewerb
"""

class Person(MinimalModel):
    """ DB-Eintrag für eine Person

    erbt nur von MinimalModel, da Link zu einem Nutzer obligatorisch ist,
    und damit ein name-Feld redundant wäre.

    TODO: bei delete vorher was machen, u.a. Teilnahmen auf string setzen
    """
    veranstaltungen = models.ManyToManyField(
        'Veranstaltung',
        through='Teilnahme',
        related_name='personen',
    )
    wettbewerbe = models.ManyToManyField(
        'WettbewerbKonkret',
        through='Erfolg',
        related_name='personen',
    )
    # TODO: vereinfachen bei upgrade auf django 1.11
    AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    nutzer = models.OneToOneField(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='person',
    )

    @classmethod
    def erstellen(cls, nutzer):
        return cls.objects.create(nutzer=nutzer)

    @property
    def name(self):
        return self.nutzer.get_full_name()
    def __str__(self):
        return 'Person {}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Personen'
        verbose_name = 'Person'


class Veranstaltung(Grundklasse):
    """ Eine konkrete Veranstaltung an einem Ort """
    art = models.ForeignKey(
        'ArtVeranstaltung',
        null=True,
        on_delete=models.PROTECT,
    )
    beschreibung = models.TextField(default='', blank=True)
    datum_anfang = models.DateField(null=True, blank=True)
    datum_ende = models.DateField(null=True, blank=True)
    class Meta: verbose_name_plural = 'Veranstaltungen'


class WettbewerbPrinzipiell(Grundklasse):
    """ Ein generisches Wettbewerbsobjekt, zeitlos

    Eine Instanz im Netz der Wettbewerbe, z.B. LaMO Sachsen 9.Klasse
    Hat in jedem Jahr ein verknüpftes WettbewerbKonkret-Objekt
    """
    slug_prefix = models.SlugField()
    datum = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    fortsetzung = models.ForeignKey(
        'WettbewerbPrinzipiell',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vorheriger',
    )
    erfolgsarten = models.ManyToManyField(
        'ArtErfolg',
        blank=True,
        related_name='wettbewerbsarten',
    )

    def get_absolute_url(self):
        return reverse('Wettbewerbe:ein_wettbewerb_generisch', kwargs=dict(
            slug_prefix=self.wettbewerb.slug_prefix,
            slug=self.wettbewerb.slug,
        ))

    class Meta:
        verbose_name = 'Generischer Wettbewerb'
        verbose_name_plural = 'Wettbewerbe Generisch'


class WettbewerbKonkret(MinimalModel):
    """ Ein konkretes Wettbewerbsobjekt, in das man sich eintragen kann

    Gehört zu einem WettbewerbGenerisch
    """
    beschreibung = models.TextField(default='', blank=True)
    jahrgang = models.PositiveSmallIntegerField()
    datum = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    wettbewerb = models.ForeignKey(
        'WettbewerbPrinzipiell',
        on_delete=models.CASCADE,
        related_name='jahrgaenge',
    )
    veranstaltung = models.ForeignKey(
        'Veranstaltung',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='wettbewerbe',
    )

    @property
    def name(self):
        if self.jahrgang < 1000:
            return "%s. %s" % (self.jahrgang, self.wettbewerb.name)
        else:
            return "%s %s" % (self.wettbewerb.name, self.jahrgang)

    def __str__(self):
        return "Jahrgang {nr} von {wettbewerb}, geändert {datum}".format(
            nr=self.jahrgang,
            wettbewerb=self.wettbewerb.name,
            datum=self.zeit_geaendert,
        )

    def get_absolute_url(self):
        return reverse('Wettbewerbe:ein_wettbewerb_konkret', kwargs=dict(
            slug_prefix=self.wettbewerb.slug_prefix,
            jahrgang=str(self.jahrgang),
            slug=self.wettbewerb.slug,
        ))

    class Meta:
        verbose_name = 'Konkreter Wettbewerb'
        verbose_name_plural = 'Wettbewerbe Konkret'


class Teilnahme(MinimalModel):
    """ Verknüpft Person mit Veranstaltung, gehört zu einer Art """
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='teilnahmen',
    )
    nur_name = models.CharField( # falls Person nicht eingetragen, nur str
        max_length=99,
        blank=True,
    )
    veranstaltung = models.ForeignKey(
        Veranstaltung,
        on_delete=models.CASCADE,
        related_name='teilnahmen',
    )
    art = models.ForeignKey(
        'ArtTeilnahme',
        on_delete=models.PROTECT,
        null=True,
    )
    ob_weitergekommen = models.BooleanField(default=False)

    @property
    def name(self):
        try:
            return self.nur_name or self.person.name
        except AttributeError:
            return "weder nur_name noch person eingetragen"

    def __str__(self):
        name = self.person or self.nur_name or '?'
        return '{} - {}'.format(name, self.veranstaltung)

    def save(self, *args, **kwargs):
        """ Führt vor dem save() Validierungen durch """
        if self.nur_name and self.person:
            raise(ValidationError(
                "Es darf nur Person *oder* nur_name eingetragen sein!"
            ))

        if not self.art in self.veranstaltung.art.teilnahmearten.all():
            raise(ValidationError(
                "Art der Teilnahme muss von Veranstaltung erlaubt sein!"
            ))

        # guckt ob bei derselben V. schon jemand mit gleichem Namen ist
        if (self.name in [t.name for t in self.veranstaltung.teilnahmen.all()]):
            raise(ValidationError(
                "Es gibt schon eine Teilnahme von {name} an {v}".format(
                    name=self.name,
                    v=self.veranstaltung,
                )
            ))

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('person', 'veranstaltung')
        verbose_name = 'Konkrete Teilnahme'
        verbose_name_plural = 'Konkrete Teilnahmen'


class Erfolg(MinimalModel):
    """ Verknüpft Person mit Wettbewerb, gehört zu einer Art """
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='erfolge',
    )
    nur_name = models.CharField( # falls Person nicht eingetragen, nur str
        max_length=99,
        blank=True,
    )
    wettbewerb = models.ForeignKey(
        WettbewerbKonkret,
        on_delete=models.CASCADE,
        related_name='erfolge',
    )
    art = models.ForeignKey(
        'ArtErfolg',
        on_delete=models.PROTECT,
        null=True,
    )

    @property
    def name(self):
        try:
            return self.nur_name or self.person.name
        except AttributeError:
            return "weder nur_name noch person eingetragen"

    def __str__(self):
        name = self.person or self.nur_name or '?'
        return '{} - {}'.format(name, self.wettbewerb)

    def save(self, *args, **kwargs):
        """ Führt vor dem save() Validierungen durch """
        if self.nur_name and self.person:
            raise(ValidationError(
                "Es darf nur Person *oder* nur_name eingetragen sein!"
            ))

        if not self.art in self.wettbewerb.wettbewerb.erfolgsarten.all():
            raise(ValidationError(
                "Art des Erfolges muss vom Wettbewerb erlaubt sein!"
            ))

        # guckt ob bei demselben W. schon jemand mit gleichem Namen ist
        if (self.name in [e.name for e in self.wettbewerb.erfolge.all()]):
            raise(ValidationError(
                "Es gibt schon einen Erfolg von {name} bei {w}".format(
                    name=self.name,
                    v=self.wettbewerb,
                )
            ))

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('person', 'wettbewerb')
        verbose_name = 'Konkreter Erfolg'
        verbose_name_plural = 'Konkrete Erfolge'


class ArtVeranstaltung(Grundklasse):
    """ Seminar, Olympiaderunde...; bestimmt, welche Teilnahmearten es gibt
    """
    teilnahmearten = models.ManyToManyField(
        'ArtTeilnahme',
        blank=True,
        related_name='veranstaltungsarten',
    )
    class Meta:
        verbose_name = 'Art von Veranstaltungen'
        verbose_name_plural = 'Arten der Veranstaltungen'

class ArtTeilnahme(Grundklasse):
    """ Bezeichnung der Art: Teilnehmer, Organisator """
    class Meta:
        verbose_name = 'Teilnahmeart'
        verbose_name_plural = 'Arten von Teilnahmen'

class ArtErfolg(Grundklasse):
    """ Bezeichnung der Art: xy.Preis, Medaille, etc """
    class Meta:
        verbose_name = 'Erfolgsart'
        verbose_name_plural = 'Arten von Erfolgen'

class ArtTag(Grundklasse):
    """ Art: Wettbewerb, Bundesland, Klassenstufe, ...? """
    class Meta:
        verbose_name = 'Art des Tags'
        verbose_name_plural = 'Arten von Tags'

class Tag(Grundklasse):
    """ Tags von Wettbewerben: Matheolympiade, Sachsen, etc. """
    art = models.ForeignKey(
        ArtTag,
        null=True,
        on_delete=models.PROTECT,
        related_name='tags',
    )
    wettbewerbe = models.ManyToManyField(
        WettbewerbPrinzipiell,
        blank=True,
        related_name='tags',
    )
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

