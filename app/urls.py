from django.urls import path
from . import views
from .views import CourseCreate, TopicCreate, OrderCreate, SuccessView

urlpatterns = [
    path('', views.home, name="home"),
    path('courses', views.courses, name="courses"),
    path('course/<int:pk>/', views.course, name="course"),
    path('cancel', views.cancel, name="cancel"),
    path('success/', views.success, name="success"),

    # path('success/', SuccessView.as_view(), name="success"),
 
    path('course_create/', CourseCreate.as_view(), name="create-course"),
    path('topics_create/', TopicCreate.as_view(), name="create-topic"),
    path('order_create/', OrderCreate.as_view(), name="create-order"),
    path('course/topic/<int:id>/', views.topic, name="topic"),
    path('webhooks/stripe/', views.webhook, name="webhook")
    
]