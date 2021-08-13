from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import AccountSerializer, AccountChangePasswordSerializer


class Register(CreateAPIView):
    serializer_class = AccountSerializer


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class PasswordChange(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        request.data['account_id'] = Token.objects.get(key=request.auth.key).user_id
        serializer = AccountChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
