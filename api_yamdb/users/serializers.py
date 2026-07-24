from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import User
from .validators import validate_username_not_me


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username_not_me,
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
        ]
    )
    email = serializers.EmailField(max_length=254, validators=[])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        email = data['email']
        username = data['username']

        if User.objects.filter(
            email=email
        ).exclude(username=username).exists():
            raise serializers.ValidationError(
                'Этот email уже используется другим пользователем.'
            )
        if User.objects.filter(
            username=username
        ).exclude(email=email).exists():
            raise serializers.ValidationError(
                'Этот username уже занят с другим email.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
