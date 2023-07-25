from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view
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
    serializer = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(author=self.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(author=self.user)


class UnfinishedTodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(author=self.user, is_read=False).order_by('-date_created')
    

class FinishedTodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(author=self.user, is_read=True).order_by('-date_created')


# class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer = TodoSerializer

#     def 