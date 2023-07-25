from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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
