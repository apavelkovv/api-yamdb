from django.urls import path
from .views import signup, get_token, MeProfileView

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token_obtain'),
    path('users/me/', MeProfileView.as_view(), name='me_profile'),
]