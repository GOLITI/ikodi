import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=email,
            email=email,
            password=make_password(password),
            first_name=name
        )

        tokens = get_tokens_for_user(user)
        return Response({
            'user': {'email': user.email, 'name': user.first_name},
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                'user': {'email': user.email, 'name': user.first_name},
                'tokens': tokens
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            email = idinfo.get('email')
            name = idinfo.get('name', '')

            if not email:
                return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create the user based on email (since Google verified it)
            user, created = User.objects.get_or_create(username=email, defaults={
                'email': email,
                'first_name': name,
            })
            
            # Optionally update the user's name if they were newly created or it changed
            if created and not user.has_usable_password():
                user.set_unusable_password()
                user.save()

            picture = idinfo.get('picture', '')

            tokens = get_tokens_for_user(user)
            return Response({
                'user': {'email': user.email, 'name': user.first_name, 'picture': picture},
                'tokens': tokens,
                'is_new': created
            })

        except ValueError as e:
            # Invalid token
            logger.error(f"Invalid Google token: {e}")
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
