from django.db import models
from catalog.models import Product
from django.conf import settings

class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CarItem.objects.create(
                cart_key=cart_key, product=product, price=product.price
            )
        return cart_item, created

class CarItem(models.Model):

    cart_key = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    product = models.ForeignKey(Product, verbose_name='Produto', null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)

class OrderManager(models.Manager):

    def create_order(self, user, cart_items):
        order = self.create(user=user)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order, product=cart_item.product, quantity=cart_item.quantity,
                price=cart_item.price
            )
        return order

class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'Aguardando pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada')
    )
    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'PayPal')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    payment_option = models.CharField(
        'Opção de pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20,
        default='deposit'
    )
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='itens', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Produto', null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    def __str__(self):
        return '[{}] {}'.format(self.order, self.product)

def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()

models.signals.post_save.connect(
    post_save_cart_item, sender=CarItem, dispatch_uid='post_save_cart_item'
)
