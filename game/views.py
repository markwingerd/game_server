from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.functions import Abs
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Character, EventTemplate, Event, Monster, ContentTag, CharacterRelationship
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import CharacterSerializer, EventTemplateSerializer, EventSerializer, MonsterSerializer, ContentTagSerializer, CharacterRelationshipSerializer, RegisterSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        accessible = self.request.query_params.get('accessible', None)
        
        if accessible:
            if user.is_authenticated:
                user_owned = Character.objects.filter(user=user).order_by('-id')
                public_owned = Character.objects.filter(user__username='public')
                queryset = user_owned | public_owned
            else:
                queryset = Character.objects.filter(user__username='public')
            return queryset

        return Character.objects.all()
    
    def perform_create(self, serializer):
        # Associate the character with the logged-in user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return detailed error messages if validation fails
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='events')
    def events(self, request, pk=None):
        character = self.get_object()
        if character.user != request.user and character.user.username != 'public':
            return Response({"detail": "Not authorized to view this character's events."}, status=403)

        events = character.events.all().order_by('-id')

        # Paginate the events
        paginator = PageNumberPagination()
        # paginator.page_size = 10  # You can adjust the page size
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='relationships')
    def relationships(self, request, pk=None):
        character = self.get_object()
        if character.user != request.user and character.user.username != 'public':
            return Response({"detail": "Not authorized to view this character's relationships."}, status=403)

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


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
