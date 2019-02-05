from django.contrib import admin

from . import models

admin.site.register(models.Person)
admin.site.register(models.Teilnahme)
admin.site.register(models.Erfolg)
admin.site.register(models.ArtTeilnahme)
admin.site.register(models.ArtErfolg)
admin.site.register(models.ArtVeranstaltung)
admin.site.register(models.ArtTag)

class OhneKommentarlisteAdmin(admin.ModelAdmin):
    exclude = ('kommentarliste', )

class ErfolgInline(admin.TabularInline):
    model = models.Erfolg
    fields = ('nur_name', 'person', 'art')
    extra = 1

class WettbewerbAdmin(OhneKommentarlisteAdmin):
    inlines = [ErfolgInline]

class TeilnahmeInline(admin.TabularInline):
    model = models.Teilnahme
    fields = ('nur_name', 'person', 'art', 'ob_weitergekommen')
    extra = 1

class WettbewerbInline(admin.StackedInline):
    model = models.WettbewerbKonkret
    exclude = ('kommentarliste', )
    extra = 1

class VeranstaltungAdmin(OhneKommentarlisteAdmin):
    inlines = [TeilnahmeInline, WettbewerbInline]

admin.site.register(models.Veranstaltung, VeranstaltungAdmin)
admin.site.register(models.WettbewerbKonkret, WettbewerbAdmin)
admin.site.register(models.WettbewerbPrinzipiell, OhneKommentarlisteAdmin)
admin.site.register(models.Tag, OhneKommentarlisteAdmin)
