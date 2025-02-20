from django.urls import path
from .views import upload_cv, candidate_view, handle_response

urlpatterns = [
    path('', upload_cv, name='upload_cv'),
    path('candidate/<int:pk>/', candidate_view, name='candidate_view'),
    path('chat/', handle_response, name='chat_prompt'),
]