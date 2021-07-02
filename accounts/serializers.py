from rest_framework import serializers
from django.db import transaction
from accounts.models import Account
from rest_framework.authtoken.models import Token


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'token']

    def create(self, validated_data):
        with transaction.atomic():
            user = Account.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )
            token = Token.objects.create(user=user)
            user.token = token.key
        return user
