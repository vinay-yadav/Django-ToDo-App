from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from todo.models import Todo
from .serializers import TodoSerializer, TodoUpdateSerializer


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.filter(username=data.get('username'))
        if user.exists():
            return JsonResponse({'userError': 'Username already exists'}, status=401)
        user = User.objects.create_user(username=data.get('username'), password=data.get('password'))
        user.save()
        token = Token.objects.create(user=user)
        login(request, user)
        return JsonResponse({'token': str(token)}, status=201)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user is None:
            return JsonResponse({'loginError': 'incorrect credential'}, status=403)
        token = Token.objects.filter(user=user)
        if token.exists():
            token.delete()
        token = Token.objects.create(user=user)
        login(request, user)
        return JsonResponse({'token': str(token)}, status=201)


class ListTodoCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user, datecompleted__isnull=True).order_by('-datecompleted')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListCompleteTodo(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(datecompleted__isnull=False, user=self.request.user).order_by('-datecompleted')


class TodoUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoCompleted(generics.UpdateAPIView):
    serializer_class = TodoUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()
