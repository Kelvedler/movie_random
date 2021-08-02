from rest_framework import serializers
from django.db import transaction
from accounts.models import Account
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password


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


class AccountChangePasswordSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField(write_only=True)
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ['account_id', 'old_password', 'new_password', 'token']

    def create(self, validated_data):
        account = Account.objects.get(pk=validated_data['account_id'])
        if check_password(password=validated_data['old_password'], encoded=account.password):
            account.set_password(validated_data['new_password'])
            account.save()
            Token.objects.filter(user_id=validated_data['account_id']).delete()
            token = Token.objects.create(user=account)
            account.token = token.key
            return account
        else:
            raise serializers.ValidationError({'message': 'Incorrect Password'})
