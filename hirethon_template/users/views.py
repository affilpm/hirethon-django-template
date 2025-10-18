from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegsiterSerialization, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RegisterView(generics.CreateAPIView):
    serializer_class = RegsiterSerialization
    permission_classes = [AllowAny]
    authentication_classes = []  
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "email": user.email,
                "name": user.name,
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class RefreshTokenView(APIView):
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get(refresh_token)  
        
        if not refresh_token:
            return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            new_refresh_token = str(refresh)
            
            return Response({"access": access_token, "refresh": new_refresh_token}, status=status.HTTP_200_OK)
        
        except:
            return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)   