from config.settings import STRIPE_KEY
import stripe
stripe.api_key = STRIPE_KEY


def create_product(product):
    product = stripe.Product.create(name=product.title)
    return product['id']


def create_price(product_id, amount):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product_id
    )
    return price['id']


def create_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.url
