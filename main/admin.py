from django.contrib import admin
from .models import Film, ExtraInfo, Ocena, Aktor


admin.site.register(Film)
admin.site.register(ExtraInfo)
admin.site.register(Ocena)
admin.site.register(Aktor)