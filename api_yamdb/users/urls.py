from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_token, signup

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token_obtain'),
    path('', include(router.urls)),
]
