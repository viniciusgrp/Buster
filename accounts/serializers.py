from rest_framework import serializers
from .models import Account
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, validators=[UniqueValidator(queryset=Account.objects.all(), message="username already taken.")])
    email = serializers.CharField(max_length=127, validators=[UniqueValidator(queryset=Account.objects.all(), message='email already registered.')])
    password = serializers.CharField(max_length=127, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(default=None)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)


    def create(self, validated_data: dict) -> Account:
        if validated_data['is_employee']:
            validated_data['is_superuser']=True
            return Account.objects.create_user(**validated_data)


        return Account.objects.create_user(**validated_data)
    

    def update(self, instance: Account, validated_data: dict) -> Account:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(validated_data['password'])

        instance.save()

        return instance