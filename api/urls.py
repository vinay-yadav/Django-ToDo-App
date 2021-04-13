from django.urls import path
from .views import *

urlpatterns = [
    path('todos/', ListTodoCreate.as_view()),
    path('todos/completed/', ListCompleteTodo.as_view()),
    path('todos/<int:pk>/update/', TodoUpdate.as_view()),
    path('todos/<int:pk>/complete/', TodoCompleted.as_view()),
    path('sign-up/', sign_up),
    path('login/', login_user)
]
