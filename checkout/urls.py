from django.urls import path
from . import views

app_name='checkout'
urlpatterns = [
    path('carrinho/adicionar/<str:slug>/', views.create_cartItem, name='create_cartitem'),
    path('carrinho/', views.cart_item, name='cart_item'),
    path('finalizando/', views.checkout, name='checkout'),
    path('finalizando/<int:pk>/pagseguro', views.pag_seguro, name='pagseguro'),
    path('finalizando/<int:pk>/paypal', views.pay_pal, name='paypal'),
    path('meus-pedidos/', views.order_list, name='order_list'),
    path('meus-pedidos/<int:pk>/', views.order_detail, name='order_detail'),
    path('notificacoes/pagseguro', views.pagseguro_notification, name='pagseguro_notification'),
]
