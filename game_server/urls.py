from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from game.views import CharacterViewSet, EventTemplateViewSet, EventViewSet, MonsterViewSet, ContentTagViewSet


router = DefaultRouter()
router.register(r'characters', CharacterViewSet, basename='character')
router.register(r'event_templates', EventTemplateViewSet)
router.register(r'events', EventViewSet)
router.register(r'monsters', MonsterViewSet)
router.register(r'content_tags', ContentTagViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]