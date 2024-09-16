from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Character, EventTemplate, Event, Monster, ContentTag, CharacterRelationship

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class ContentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTag
        fields = '__all__'

class EventTemplateSerializer(serializers.ModelSerializer):
    content_tags = ContentTagSerializer(many=True, read_only=True)

    class Meta:
        model = EventTemplate
        fields = '__all__'

class MonsterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monster
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    template = EventTemplateSerializer(read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    monsters = MonsterSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

class CharacterRelationshipSerializer(serializers.ModelSerializer):
    to_character_name = serializers.CharField(source='to_character.first_name', read_only=True)

    class Meta:
        model = CharacterRelationship
        fields = ['id', 'to_character', 'to_character_name', 'friendship_rivalry', 'knows_about']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user