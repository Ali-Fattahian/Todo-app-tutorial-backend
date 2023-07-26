from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from .serializers import TodoSerializer
from .models import Todo


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not (username and password): # If either of them is empty
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password) # Returns user if authentication was successfull
    if user: # Success
        token = Token.objects.get_or_create(user=user) # Tuple like this: (token, created-or-not)
        return Response(str(token[0]), status=status.HTTP_200_OK)
    
    return Response({'error': 'Username or password is wrong'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not (username and password):
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 5:
        return Response({'error': 'Password must be at least 5 characters long'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_model().objects.create_user(username=username, password=password) # User is created

    if user:
        token = Token.objects.get_or_create(user=user)
        return Response(str(token[0]), status=status.HTTP_200_OK)
    
    return Response({'error': 'Please choose a different username'}, status=status.HTTP_400_BAD_REQUEST)


class TodoListView(generics.ListCreateAPIView):
    """Returns all todos finished and unfinished"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UnfinishedTodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user, is_read=False).order_by('-date_created')
    

class FinishedTodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user, is_read=True).order_by('-date_created')


# class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer = TodoSerializer

#     def 


@permission_classes([permissions.IsAuthenticated])
@api_view(['PUT'])
def change_todo_to_read(request, pk):
    todo = get_object_or_404(Todo, pk=pk)

    if request.user == todo.author:
        todo.is_read = True
        todo.save()
        serializer = TodoSerializer(todo)
        return Response({'todo': serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': 'You are not allowed to do this action'}, status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([permissions.IsAuthenticated])
@api_view(['PUT'])
def change_todo_to_unread(request, pk):
    todo = get_object_or_404(Todo, pk=pk)

    if request.user == todo.author:
        todo.is_read = False
        todo.save()
        serializer = TodoSerializer(todo)
        return Response({'todo': serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': 'You are not allowed to do this action'}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteTodoView(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You are not allowed to do this action'}, status=status.HTTP_401_UNAUTHORIZED)
