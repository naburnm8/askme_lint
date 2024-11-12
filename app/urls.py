
from django.urls import path, include
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>', views.question, name='question'),
]
