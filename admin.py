from django.contrib import admin

from . import models

admin.site.register(models.Person)
admin.site.register(models.Veranstaltung)
admin.site.register(models.Wettbewerb)
admin.site.register(models.Teilnahme)
admin.site.register(models.Erfolg)
admin.site.register(models.ArtTeilnahme)
admin.site.register(models.ArtErfolg)
admin.site.register(models.ArtVeranstaltung)
admin.site.register(models.ArtWettbewerb)
