from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('courses', views.courses, name="courses"),
    path('course/<int:pk>/', views.course, name="course"),
    path('cancel', views.cancel, name="cancel"),
    path('success/', views.success, name="success"),
    path('course/topic/<int:id>/', views.topic, name="topic"),
    path('webhooks/stripe/', views.webhook, name="webhook")
    
]