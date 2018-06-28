from django.urls import path
from .views import register, index, update_user, update_password

app_name = 'accounts'
urlpatterns = [
    path('', index, name='index'),
    path('registro/', register, name='register'),
    path('alterar-dados/', update_user, name='update_user'),
    path('alterar-senha/', update_password, name='update_password'),
]
