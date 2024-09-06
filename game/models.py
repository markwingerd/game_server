from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Event(models.Model):
    template = models.ForeignKey('EventTemplate', on_delete=models.CASCADE)
    characters = models.ManyToManyField('Character', related_name='events', blank=True)
    monsters = models.ManyToManyField('Monster', related_name='events', blank=True)
    tick_count = models.IntegerField()

    def __str__(self):
        return f'Event: {self.template.name}'

class Character(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    hp_max = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    hp = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    attack = models.IntegerField(default=10,validators=[MinValueValidator(1), MaxValueValidator(100)])
    defense = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    speed = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    dexterity = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    willpower = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    intelligence = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    rest = models.IntegerField(default=1000, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    food = models.IntegerField(default=1000, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    social = models.IntegerField(default=1000, validators=[MinValueValidator(0), MaxValueValidator(1000)])  # New social attribute

    def current_event(self):
        return self.events.last()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Monster(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    hp_max = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    hp = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    attack = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    defense = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    speed = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    dexterity = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    willpower = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    intelligence = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def current_event(self):
        return self.events.last()

    def __str__(self):
        return self.name

class EventTemplate(models.Model):
    name = models.CharField(max_length=100)
    event_texts = models.JSONField(default=list)  # List of text fields
    max_characters = models.PositiveIntegerField(default=1)
    max_enemies = models.PositiveIntegerField(default=1)
    content_tags = models.ManyToManyField('ContentTag', related_name='event_templates')

    def __str__(self):
        return self.name

class ContentTag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class GameState(models.Model):
    current_tick = models.IntegerField(default=0)

    def __str__(self):
        return f'Current Tick: {self.current_tick}'
    
    @classmethod
    def get_current_tick(cls):
        # Ensure there is always exactly one GameState entry
        obj, created = cls.objects.get_or_create(id=1)
        return obj.current_tick
    
    @classmethod
    def increment_tick(cls, ticks=1):
        obj, created = cls.objects.get_or_create(id=1)
        obj.current_tick += ticks
        obj.save()
        return obj.current_tick