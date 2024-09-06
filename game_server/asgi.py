import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # WebSocket support can be added here later if needed
})