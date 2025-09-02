from django.urls import path
from .views import ChatMessageListView, ChatMessageCreateView, MarkMessageReadView

urlpatterns = [
    path("messages/<int:batch_id>/", ChatMessageListView.as_view(), name="chat-messages"),
    path("messages/create/", ChatMessageCreateView.as_view(), name="chat-message-create"),
    path("messages/<int:pk>/read/", MarkMessageReadView.as_view(), name="chat-message-read"),
]
