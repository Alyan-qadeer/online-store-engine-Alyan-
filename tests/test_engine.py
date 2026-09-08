from src.models import Product, ShoppingCart, OrderClearinghouse


def test_duplicate_product_rejected():
    product = Product("P1", "Keyboard", 120.0, 5)

    cart = ShoppingCart("CART-101", "USR-808")

    assert cart.add_product(product) is True
    assert cart.add_product(product) is False
    assert len(cart.items) == 1


def test_update_quantity_zero_sets_out_of_stock():
    product = Product("P1", "Keyboard", 120.0, 5)

    product.update_quantity(0)

    assert product.quantity == 0
    assert product.is_out_of_stock is True


def test_empty_cart_checkout_rejected():
    clearinghouse = OrderClearinghouse(5000.0)
    cart = ShoppingCart("CART-101", "USR-808")

    initial_balance = clearinghouse.gateway_balance

    assert clearinghouse.process_checkout(cart) is False
    assert clearinghouse.gateway_balance == initial_balance


def test_duplicate_cart_checkout_rejected():
    clearinghouse = OrderClearinghouse(5000.0)

    product = Product("P1", "Keyboard", 120.0, 5)

    cart = ShoppingCart("CART-101", "USR-808")
    cart.add_product(product)

    assert clearinghouse.process_checkout(cart) is True

    balance_after_first = clearinghouse.gateway_balance

    duplicate_cart = ShoppingCart("CART-101", "USR-808")
    duplicate_cart.add_product(product)

    assert clearinghouse.process_checkout(duplicate_cart) is False
    assert clearinghouse.gateway_balance == balance_after_first
