from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/(?P<poll_id>\w+)/$", consumers.PollStatsConsumer.as_asgi()),
]
