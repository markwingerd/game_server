from django.contrib import admin
from .models import Character, EventTemplate, Event, Monster, ContentTag

admin.site.register(Character)
admin.site.register(EventTemplate)
admin.site.register(Event)
admin.site.register(Monster)
admin.site.register(ContentTag)