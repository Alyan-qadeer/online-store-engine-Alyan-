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

    result = clearinghouse.process_checkout(cart)

    assert result is False
    assert clearinghouse.gateway_balance == initial_balance


def test_duplicate_cart_id_rejected():
    clearinghouse = OrderClearinghouse(5000.0)

    cart = ShoppingCart("CART-101", "USR-808")

    product = Product("P1", "Keyboard", 120.0, 5)

    cart.add_product(product)

    first_result = clearinghouse.process_checkout(cart)

    initial_balance = clearinghouse.gateway_balance

    second_result = clearinghouse.process_checkout(cart)

    assert first_result is True
    assert second_result is False
    assert clearinghouse.gateway_balance == initial_balance
