import json
import os
from decouple import config
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from game.models import Character, EventTemplate, Event, Monster, ContentTag
from django.conf import settings
import random

class Command(BaseCommand):
    help = 'Seed the database with initial data from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'game_server/management/commands/seed_data.json')
        with open(file_path, 'r') as file:
            data = json.load(file)

        self.clear_data()
        self.create_users(data['users'])
        self.create_content_tags(data['content_tags'])
        self.create_event_templates(data['event_templates'])
        self.create_monsters(data['monsters'])
        self.create_characters(data['characters'])
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def clear_data(self):
        """Delete all data from the database."""
        User.objects.all().delete()
        Character.objects.all().delete()
        EventTemplate.objects.all().delete()
        Event.objects.all().delete()
        Monster.objects.all().delete()
        ContentTag.objects.all().delete()

    def create_users(self, users_data):
        """Create users from JSON data and passwords from .env file."""
        self.users = {}
        for user_data in users_data:
            # Load password from the .env file using the username as the key
            password = config(f"{user_data['username'].upper()}_PASSWORD", default='defaultpassword')
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password
            )
            self.users[user_data['username']] = user

    def create_content_tags(self, tags_data):
        """Create content tags from JSON data."""
        self.tags = {}
        for tag_data in tags_data:
            tag = ContentTag.objects.create(
                name=tag_data['name'],
                description=tag_data['description']
            )
            self.tags[tag_data['name']] = tag

    def create_event_templates(self, templates_data):
        """Create event templates from JSON data."""
        self.templates = []
        for template_data in templates_data:
            template = EventTemplate.objects.create(
                name=template_data['name'],
                max_characters=template_data['max_characters'],
                max_enemies=template_data['max_enemies'],
                event_texts=template_data['event_texts'],
                event_function=template_data['event_function'],
                event_kwargs=template_data['event_kwargs'],
                social_effects=template_data['social_effects'],
            )
            template.content_tags.add(self.tags[template_data['content_tag']])
            self.templates.append(template)

    def create_monsters(self, monsters_data):
        """Create monsters from JSON data."""
        self.monsters = []
        for monster_data in monsters_data:
            monster = Monster.objects.create(
                name=monster_data['name'],
                description=monster_data['description'],
                hp_max=monster_data['hp_max'],
                hp=monster_data['hp'],
                attack=monster_data['attack'],
                defense=monster_data['defense']
            )
            self.monsters.append(monster)

    def create_characters(self, characters_data):
        """Create characters from JSON data."""
        self.characters = []
        for char_data in characters_data:
            character = Character.objects.create(
                user=self.users[char_data['user']],
                first_name=char_data['first_name'],
                last_name=char_data['last_name'],
                age=char_data['age'],
                sex=char_data['sex'],
                height=char_data['height'],
                weight=char_data['weight'],
                muscles=char_data['muscles'],
                hp_max=char_data['hp_max'],
                hp=char_data['hp'],
                attack=char_data['attack'],
                defense=char_data['defense']
            )
            self.characters.append(character)