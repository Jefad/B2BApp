from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

import pathlib
import json

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer

User = get_user_model()

cred_path = pathlib.Path("/log_reg/creds.json")


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user_serializer = UserSerializer(user)
        return Response({'access_token': access_token, 'refresh_token': refresh_token,
                         'user': user_serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user=user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            token_data = {
                "refresh": refresh_token,
                "access": access_token
            }

            serializer = UserSerializer(user)

            try:
                cred_path.write_text(json.dumps(token_data))
                print("The token data was written to the creds file.")
            except:
                raise Exception("Error in writing token data!")

            return Response({'access_token': access_token, 'refresh_token': refresh_token,
                             'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            RefreshToken(refresh_token).blacklist()

            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})
