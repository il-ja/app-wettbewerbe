from django.contrib import admin

from . import models

admin.site.register(models.Person)
admin.site.register(models.Veranstaltung)
admin.site.register(models.WettbewerbPrinzipiell)
admin.site.register(models.WettbewerbKonkret)
admin.site.register(models.Teilnahme)
admin.site.register(models.Erfolg)
admin.site.register(models.ArtTeilnahme)
admin.site.register(models.ArtErfolg)
admin.site.register(models.ArtVeranstaltung)
admin.site.register(models.ArtTag)
admin.site.register(models.Tag)
