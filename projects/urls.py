from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

app_name = "projects"

urlpatterns = [
    path("", views.index, name="index"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path('post/<int:project_id>/', views.project_detail, name='project_detail'),
    path('toggle_like/<int:project_id>/', views.toggle_like, name='toggle_like'),
    path('start-conversation/<int:recipient_id>/', views.start_conversation, name='start_conversation'),
    path('contact/', views.contact, name="contact"),
    path('conversation-detail/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('inbox/', views.inbox, name='inbox'),  # Add this line

    # Add other URL patterns as needed
]
