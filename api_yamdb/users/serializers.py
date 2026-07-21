from rest_framework import serializers
from .models import User
from .validators import validate_username_not_me
from rest_framework_simplejwt.tokens import AccessToken


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username_not_me])
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if User.objects.filter(email=data['email']).exclude(username=data['username']).exists():
            raise serializers.ValidationError('Этот email уже используется другим пользователем.')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден.')

        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения.')

        token = AccessToken.for_user(user)
        return {'token': str(token)}


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
