from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.db import models
from django_extensions.db.models import TimeStampedModel
from Grundgeruest.models import Grundklasse
from Kommentare.models import KommentareMetaklasse


""" Es werden folgende models definiert:
 - Person
 - Veranstaltung
 - Wettbewerb - Konkret und Prinzipiell - und Tag
 - Teilnahme, Erfolg
 - ArtTeilnahme, ArtErfolg, ArtVeranstaltung, ArtTag
"""

class Person(TimeStampedModel):
    """ DB-Eintrag für eine Person

    erbt nur von TimeStampedModel, da Link zu einem Nutzer obligatorisch ist,
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
    nutzer = models.OneToOneField(
        get_user_model(),
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
        return "%s %s" % (self.nutzer.profil.vorname, self.nutzer.profil.nachname)
    @property
    def title(self):
        return self.name
    def __str__(self):
        return 'Person {}'.format(self.name)

    def get_absolute_url(self):
        return reverse('Wettbewerbe:eine_person', kwargs=dict(
            pk=self.pk,
        ))

    class Meta:
        verbose_name_plural = 'Personen'
        verbose_name = 'Person'


class Veranstaltung(Grundklasse, metaclass=KommentareMetaklasse):
    """ Eine konkrete Veranstaltung an einem Ort """
    art = models.ForeignKey(
        'ArtVeranstaltung',
        null=True,
        on_delete=models.PROTECT,
    )
    datum_anfang = models.DateField(null=True, blank=True)
    datum_ende = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='veranstaltungen',
    )

    class Meta: verbose_name_plural = 'Veranstaltungen'

    def get_absolute_url(self):
        return reverse('Wettbewerbe:eine_veranstaltung', kwargs=dict(
            slug=self.slug,
        ))


class WettbewerbPrinzipiell(Grundklasse, metaclass=KommentareMetaklasse):
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
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='wettbewerbe',
    )
    wichtung = models.PositiveSmallIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('Wettbewerbe:ein_wettbewerb_generisch', kwargs=dict(
            slug_prefix=self.wettbewerb.slug_prefix,
            slug=self.wettbewerb.slug,
        ))

    @classmethod
    def objekt_aus_kwargs(cls, kwargs):
        wettbewerb = get_object_or_404(
            cls,
            slug=kwargs['slug'],
            slug_prefix=kwargs['slug_prefix'],
        )
        return wettbewerb

    class Meta:
        verbose_name = 'Generischer Wettbewerb'
        verbose_name_plural = 'Wettbewerbe Generisch'
        unique_together = ('slug', 'slug_prefix')


class WettbewerbKonkret(TimeStampedModel, metaclass=KommentareMetaklasse):
    """ Ein konkretes Wettbewerbsobjekt, in das man sich eintragen kann

    Gehört zu einem WettbewerbGenerisch
    """
    description = models.TextField(default='', blank=True)
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
    def title(self):
        if self.jahrgang < 1000:
            return "%s. %s" % (self.jahrgang, self.wettbewerb.title)
        else:
            return "%s %s" % (self.wettbewerb.title, self.jahrgang)

    def __str__(self):
        return "Jahrgang {nr} von {wettbewerb}, zuletzt geändert {datum}".format(
            nr=self.jahrgang,
            wettbewerb=self.wettbewerb.title,
            datum=self.modified,
        )

    def get_absolute_url(self):
        return reverse('Wettbewerbe:ein_wettbewerb_konkret', kwargs=dict(
            slug_prefix=self.wettbewerb.slug_prefix,
            jahrgang=str(self.jahrgang),
            slug=self.wettbewerb.slug,
        ))

    @classmethod
    def objekt_aus_kwargs(cls, kwargs):
        wettbewerb = WettbewerbPrinzipiell.objekt_aus_kwargs(kwargs)
        return get_object_or_404(
            wettbewerb.jahrgaenge,
            jahrgang=int(kwargs['jahrgang']),
        )

    class Meta:
        verbose_name = 'Konkreter Wettbewerb'
        verbose_name_plural = 'Wettbewerbe Konkret'


class Verknuepfung(TimeStampedModel):
    nur_name = models.CharField( # falls Person nicht eingetragen, nur str
        max_length=99,
        blank=True,
    )
    ########### das sollten erbende Klassen neben ihren model-fields definieren:
    def erlaubte_arten(self):
        return self.veranstaltung.art.teilnahmearten.all()

    verknuepft = ('veranstaltung', Veranstaltung)

    @classmethod
    def neu_zu_objekt(cls, objekt):
        """ Erstellt eine Instanz mit verknüpften objekt, ohne zu speichern

        muss so unDRY definiert werden, da der normale Konstruktor keine
        positional arguments akzeptiert und auch self.verknuepft[1] als
        key nicht zulässig ist.
        """
        return cls(veranstaltung=objekt)
    ############
    @classmethod
    def erstellen(cls, person, objekt):
        instanz = cls.neu_zu_objekt(objekt)
        instanz.person = person
        return instanz

    @property
    def objekt(self):
        return getattr(self, self.verknuepft[0])

    @property
    def name(self):
        try:
            return self.nur_name or self.person.name
        except AttributeError:
            return "weder nur_name noch person eingetragen"

    def __str__(self):
        name = self.person or self.nur_name or '?'
        return '{} - {}'.format(name, self.objekt)


    def save(self, *args, **kwargs):
        """ Führt vor dem save() Validierungen durch """
        if self.nur_name and self.person:
            raise(ValidationError(
                "Es darf nur Person *oder* nur_name eingetragen sein!"
            ))

        if not self.art in self.erlaubte_arten():
            raise(ValidationError(
                "Art muss von %s erlaubt sein!" % self.__class__.__name__
            ))

        # guckt ob bei demselben „Event“ schon jemand mit gleichem Namen ist
        if (self.name in [t.name for t in self.objekt.personen.all()]):
            raise(ValidationError(
                "Es gibt schon eine Teilnahme von {name} an {event}".format(
                    name=self.name,
                    event=self.objekt,
                )
            ))

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Teilnahme(Verknuepfung):
    """ Verknüpft Person mit Veranstaltung, gehört zu einer Art """
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='teilnahmen',
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

    ############ das braucht die parent-Klasse zum weiterverarbeiten
    verknuepft = ('veranstaltung', Veranstaltung)

    @classmethod
    def neu_zu_objekt(cls, objekt):
        return cls(veranstaltung=objekt)

    def erlaubte_arten(self):
        return self.veranstaltung.art.teilnahmearten.all()
    ############

    class Meta:
        unique_together = ('person', 'veranstaltung')
        verbose_name = 'Konkrete Teilnahme'
        verbose_name_plural = 'Konkrete Teilnahmen'


class Erfolg(Verknuepfung):
    """ Verknüpft Person mit Wettbewerb, gehört zu einer Art """
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='erfolge',
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
    zusatz = models.CharField(
        max_length=99,
        blank=True,
        default='',
    ) # für Sonderpreise, Delegierungen und Spam

    ############ das braucht die parent-Klasse zum weiterverarbeiten
    verknuepft = ('wettbewerb', WettbewerbKonkret)

    @property
    def name(self):
        if self.zusatz:
            return "%s, %s" % (self.art.title, self.zusatz)
        else:
            return self.art.title


    @classmethod
    def neu_zu_objekt(cls, objekt):
        return cls(wettbewerb=objekt)

    def erlaubte_arten(self):
        return self.wettbewerb.wettbewerb.erfolgsarten.all()
    #############

    class Meta:
        unique_together = ('person', 'wettbewerb')
        verbose_name = 'Konkreter Erfolg'
        verbose_name_plural = 'Konkrete Erfolge'

    def siegpunkte_ausgeben(self):
        return self.wettbewerb.wettbewerb.wichtung * self.art.wichtung

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
    wichtung = models.PositiveSmallIntegerField(default=0)
    class Meta:
        verbose_name = 'Erfolgsart'
        verbose_name_plural = 'Arten von Erfolgen'

class ArtTag(Grundklasse):
    """ Art: Wettbewerb, Bundesland, Klassenstufe, ...? """
    plural = models.CharField(
        max_length=99,
        blank=True,
        default='',
    )
    class Meta:
        verbose_name = 'Art des Tags'
        verbose_name_plural = 'Arten von Tags'

class Tag(Grundklasse, metaclass=KommentareMetaklasse):
    """ Tags von Wettbewerben: Matheolympiade, Sachsen, etc. """
    art = models.ForeignKey(
        ArtTag,
        null=True,
        on_delete=models.PROTECT,
        related_name='tags',
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('Wettbewerbe:ein_tag', kwargs=dict(
            slug=self.slug,
        ))

    def __str__(self):
        return '%s: %s' % (self.art, self.title)

    def rangliste_ausgeben(self):
        rangliste = {}
        for person in Person.objects.all():
            rangliste[person.pk] = 0
        for erfolg in Erfolg.objects.exclude(
                person=None).filter(
                wettbewerb__wettbewerb__tags=self):
            rangliste[erfolg.person.pk] += erfolg.siegpunkte_ausgeben()
        pks = [pk for pk in rangliste if rangliste[pk]]
        personen = Person.objects.filter(pk__in=pks)
        rangliste = sorted(
            [(person, rangliste[person.pk]) for person in personen],
            key=lambda item: -item[1]
        ) 
        return rangliste
