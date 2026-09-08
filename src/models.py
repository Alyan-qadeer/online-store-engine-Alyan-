class Product:
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        quantity: int,
        is_clearance: bool = False
    ):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.is_clearance = is_clearance

        self.is_out_of_stock = (self.quantity == 0)
        self.is_discount_eligible = (
            self.price > 100.0 and not self.is_clearance
        )

    def update_quantity(self, new_quantity: int) -> None:
        self.quantity = new_quantity
        self.is_out_of_stock = (self.quantity == 0)
        self.is_discount_eligible = (
            self.price > 100.0 and not self.is_clearance
        )


class ShoppingCart:
    def __init__(self, cart_id: str, user_id: str):
        self.cart_id = cart_id
        self.user_id = user_id

        self.items: list[Product] = []
        self.item_ids: set[str] = set()

    def add_product(self, product: Product) -> bool:
        if product is None:
            return False

        if product.product_id in self.item_ids:
            return False

        self.item_ids.add(product.product_id)
        self.items.append(product)

        return True

    def calculate_subtotal(self) -> float:
        return sum(product.price for product in self.items)


class OrderClearinghouse:
    def __init__(self, gateway_balance: float):
        self.gateway_balance = gateway_balance
        self.processed_orders: dict[str, float] = {}

    def _record_transaction(
        self,
        cart_id: str,
        amount: float
    ) -> None:
        self.processed_orders[cart_id] = amount
        self.gateway_balance += amount

    def process_checkout(
        self,
        cart: ShoppingCart,
        promo_code: str | None = None
    ) -> bool:

        if cart is None or len(cart.items) == 0:
            return False

        if cart.cart_id in self.processed_orders:
            return False

        if self.gateway_balance < cart.calculate_subtotal():
            return False

        final_amount = cart.calculate_subtotal()

        if promo_code == "SAVE20":
            final_amount = final_amount * 0.80

        self._record_transaction(cart.cart_id, final_amount)

        return True
