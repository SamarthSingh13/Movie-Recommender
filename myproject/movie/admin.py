from django.contrib import admin
from .models import Show, Ott, Genre, Language, Country, Person, CastMember, CrewMember

# Register your models here.
admin.site.register(Show)
#admin.site.register(Episode)
admin.site.register(Ott)
admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Country)
