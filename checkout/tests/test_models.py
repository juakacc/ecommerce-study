from django.test import TestCase
from django.conf import settings
from model_mommy import mommy
from checkout.models import CarItem, Order

class CartItemTestCase(TestCase):

    def setUp(self):
        mommy.make(CarItem, _quantity=3)

    def test_post_save_cart_item(self):
        cart_item = CarItem.objects.all()[0]
        cart_item.quantity = 0
        cart_item.save()
        self.assertEquals(CarItem.objects.count(), 2)

class OrderTestCase(TestCase):

    def setUp(self):
        self.cart_item = mommy.make(CarItem)
        self.user = mommy.make(settings.AUTH_USER_MODEL)

    def test_create_order(self):
        Order.objects.create_order(self.user, [self.cart_item])
        self.assertEquals(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEquals(order.user, self.user)
        order_item = order.itens.get()
        self.assertEquals(order_item.product, self.cart_item.product)
