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

    event_function = models.CharField(max_length=100, blank=True, null=True)
    event_kwargs = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def execute_event_function(self, event):
        """
        This will call the function stored in 'event_function' with optional arguments
        and apply it to each character in the event.
        """
        if self.event_function:
            func = getattr(self, self.event_function, None)
            print(func)
            if func:
                func(event, **self.event_kwargs)

    def fight(self, event, character, attack_multiplier=1, **kwargs):
        """
        event:
        character: Aggressor
        opponent: Damage taker
        """
        character = event.character[0]
        opponent = event.characters[1]
        damage_dealt = int(character.strength * attack_multiplier / opponent.defense)
        opponent.hp = max(0, opponent.hp - damage_dealt)
        character.save()
        opponent.save()
        # TODO: if character has died, try triggering a death event on this tick
        # TODO: It'd be nice to add a report json for the FE to display

    def social(self, event, social_points=50, **kwargs):
        """
        A social event function that increases social points.
        """
        for character in event.characters.all():
            character.social = max(0, min(1000, character.social + social_points))
            character.save()

    def eat(self, event, food_points, **kwargs):
        for character in event.characters.all():
            character.food = max(0, min(1000, character.food + food_points))
            character.save()

    def rest(self, event, rest_points, **kwargs):
        for character in event.characters.all():
            character.rest = max(0, min(1000, character.rest + rest_points))
            character.save()

    def work(self, event, work_points, **kwargs):
        for character in event.characters.all():
            character.rest = max(0, min(1000, character.rest - work_points))
            character.save()

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