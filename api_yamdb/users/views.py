from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
import secrets

from .models import User
from .serializers import SignUpSerializer, TokenSerializer, MeSerializer, UserSerializer
from .permissions import IsAdmin


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if not created:
        user.email = email


    confirmation_code = secrets.token_urlsafe(20)
    user.confirmation_code = confirmation_code
    user.save()

    # отправляем письмо (пока в консоль)
    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )

    return Response({'email': user.email, 'username': user.username}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MeProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    search_fields = ('username',)
