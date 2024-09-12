import random

from django.utils import timezone

from celery import shared_task
from .models import Character, Event, EventTemplate, Monster, GameState


@shared_task
def update_game_state():
    # Increment the global tick count
    current_tick = GameState.increment_tick()

    # Get all characters and shuffle them for random processing
    characters = list(Character.objects.all())
    random.shuffle(characters)

    # Iterate through characters and update their state
    while characters:
        character = characters.pop()
        handle_events(character, characters, current_tick)  # Handle event assignment
        update_needs(character, current_tick)  # Update the character's needs


def update_needs(character, current_tick):
    # Decrease food need
    character.food -= 10
    if character.food < 0:
        character.food = 0

    # Decrease rest need, more at night (assuming night is between ticks 72-95)
    # current_tick = get_current_tick()
    if 72 <= current_tick % 96 <= 95:
        character.rest -= 15  # Night time is less efficient for resting
    else:
        character.rest -= 10
    if character.rest < 0:
        character.rest = 0

    # Decrease social need
    character.social -= 5
    if character.social < 0:
        character.social = 0

    character.save()


def handle_events(character, characters, current_tick):
    """
    Selects an event and adds characters to it
    character: The currently chosen character
    characters: A pool of characters that dont have events applied to them
    current_tick: the current tick of the game
    """
    # print(f"CHARACTER {character}")
    # Step 3: Select a random EventTemplate
    event_template = EventTemplate.objects.filter(max_characters__lte=len(characters)+1).order_by('?').first()
    if not event_template:
        print(f"No event templates???")
        return  # Skip if no event templates are available

    # Step 4: Create a new Event using the selected template
    event = Event.objects.create(template=event_template, tick_count=current_tick)
    event.characters.add(character)

    # Step 5: Fill remaining slots for characters if any
    remaining_character_slots = event_template.max_characters - 1
    # available_characters = characters[:remaining_character_slots]
    # print(f"available_characters {available_characters}")
    # characters = characters[remaining_character_slots:]
    # print(f"characters {len(characters)} {characters}")
    # print(f"available_characters {available_characters}")
    available_characters = []
    for _ in range(remaining_character_slots):
        available_characters.append(characters.pop())
        
    for extra_character in available_characters:
        event.characters.add(extra_character)
        update_needs(extra_character, current_tick)
        extra_character.save()

    # Step 6: Add Monsters if there's room
    remaining_monster_slots = event_template.max_enemies
    available_monsters = Monster.objects.order_by('?')[:remaining_monster_slots]
    for monster in available_monsters:
        event.monsters.add(monster)

    event_template.execute_event_function(event)
    event.save()
    character.events.add(event)
    character.save()


# def get_current_tick():
#     # Dummy function to return the current tick (this should be replaced with your actual logic)
#     return (timezone.now().timestamp() // (15 * 60)) % 96  # Example calculation
