from flask import Flask, render_template, request, redirect, url_for
from models import Product, ShoppingCart, OrderClearinghouse

app = Flask(__name__)

# Initialize domain entities & store
clearinghouse = OrderClearinghouse(gateway_balance=5000.0)

cart = ShoppingCart(
    cart_id="CART-101",
    user_id="USR-808"
)

# Inventory Catalog
catalog = {
    "P1": Product(
        "P1",
        "Mechanical Keyboard",
        120.0,
        5,
        is_clearance=False
    ),
    "P2": Product(
        "P2",
        "Wireless Mouse",
        45.0,
        10,
        is_clearance=False
    ),
    "P3": Product(
        "P3",
        "USB-C Hub",
        25.0,
        0,
        is_clearance=True
    ),
}

# Initial quantity sync
for p in catalog.values():
    p.update_quantity(p.quantity)


@app.route("/", methods=["GET"])
def dashboard():
    return render_template(
        "index.html",
        catalog=catalog.values(),
        cart=cart,
        subtotal=cart.calculate_subtotal(),
        clearinghouse=clearinghouse,
        message=request.args.get("message")
    )


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    product = catalog.get(product_id)

    if not product or product.is_out_of_stock:
        return redirect(
            url_for(
                "dashboard",
                message="Item unavailable or out of stock."
            )
        )

    success = cart.add_product(product)

    msg = (
        "Product added successfully!"
        if success
        else "Duplicate item rejected by $O(1)$ set guard."
    )

    return redirect(
        url_for("dashboard", message=msg)
    )


@app.route("/checkout", methods=["POST"])
def checkout():
    promo_code = request.form.get("promo_code")

    success = clearinghouse.process_checkout(
        cart,
        promo_code
    )

    msg = (
        "Checkout completed successfully!"
        if success
        else "Checkout failed (empty cart or settlement error)."
    )

    return redirect(
        url_for("dashboard", message=msg)
    )


if __name__ == "__main__":
    app.run(debug=True)
