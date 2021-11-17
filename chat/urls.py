from django.urls import path
from chat.views import messages_page

urlpatterns = [
    path('', messages_page, name='message-index'),
]
