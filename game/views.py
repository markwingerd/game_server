from django.db.models import F
from django.db.models.functions import Abs
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .models import Character, EventTemplate, Event, Monster, ContentTag, CharacterRelationship
from .serializers import CharacterSerializer, EventTemplateSerializer, EventSerializer, MonsterSerializer, ContentTagSerializer, CharacterRelationshipSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    @action(detail=True, methods=['get'], url_path='events')
    def events(self, request, pk=None):
        character = self.get_object()
        events = character.events.all().order_by('-id')

        # Paginate the events
        paginator = PageNumberPagination()
        paginator.page_size = 10  # You can adjust the page size
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='relationships')
    def relationships(self, request, pk=None):
        character = self.get_object()
        relationships = CharacterRelationship.objects.filter(from_character=character).annotate(
            abs_friendship_rivalry=Abs(F('friendship_rivalry'))
        ).order_by('-abs_friendship_rivalry')

        # Paginate the relationships
        paginator = PageNumberPagination()
        paginator.page_size = 100
        paginated_relationships = paginator.paginate_queryset(relationships, request)
        serializer = CharacterRelationshipSerializer(paginated_relationships, many=True)
        return paginator.get_paginated_response(serializer.data)


class EventTemplateViewSet(viewsets.ModelViewSet):
    queryset = EventTemplate.objects.all()
    serializer_class = EventTemplateSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class MonsterViewSet(viewsets.ModelViewSet):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer


class ContentTagViewSet(viewsets.ModelViewSet):
    queryset = ContentTag.objects.all()
    serializer_class = ContentTagSerializer


    