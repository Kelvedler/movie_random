from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import AccountSerializer, AccountChangePasswordSerializer
from drf_spectacular.views import extend_schema
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import OpenApiExample


class Register(CreateAPIView):
    serializer_class = AccountSerializer


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=AccountSerializer, responses=AccountSerializer, examples=[OpenApiExample(
        name="response", value={None})])
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class PasswordChange(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter("old_password", OpenApiTypes.PASSWORD, OpenApiParameter.QUERY),
                               OpenApiParameter("new_password", OpenApiTypes.PASSWORD, OpenApiParameter.QUERY)],
                   request=AccountSerializer, responses=AccountSerializer, examples=[OpenApiExample(request_only=True,
                                                                       name='request', value={"old_password": "string",
                                                                                             "new_password": "string"}),
                                                        OpenApiExample(response_only=True,
                                                                       name='response', value={"token": "string"})])
    def post(self, request, format=None):
        request.data['account_id'] = Token.objects.get(key=request.auth.key).user_id
        serializer = AccountChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
