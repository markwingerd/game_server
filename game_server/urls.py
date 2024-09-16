from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from game.views import CharacterViewSet, EventTemplateViewSet, EventViewSet, MonsterViewSet, ContentTagViewSet, RegisterView



router = DefaultRouter()
router.register(r'characters', CharacterViewSet, basename='character')
router.register(r'event_templates', EventTemplateViewSet)
router.register(r'events', EventViewSet)
router.register(r'monsters', MonsterViewSet)
router.register(r'content_tags', ContentTagViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/signup/', RegisterView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]