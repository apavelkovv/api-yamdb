from django.urls import include, path

from .views import get_token, signup


urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token_obtain'),
]
