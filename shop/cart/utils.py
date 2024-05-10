from django.db import models

from cart.models import Cart


def recalc_cart(cart: Cart):
    """
    Функция пересчета суммы покупок в корзине
    """
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))

    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0

    cart.total_products = cart_data['id__count']
    cart.save()
