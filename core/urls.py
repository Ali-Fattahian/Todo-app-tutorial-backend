from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('todo-list', views.TodoListView.as_view(), name='todo-list'),
    path('todo-list-unfinished', views.UnfinishedTodoListView.as_view(), name='todo-list-unfinished'),
    path('todo-list-finished', views.FinishedTodoListView.as_view(), name='todo-list-finished'),
]
