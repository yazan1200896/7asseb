from fastapi import FastAPI
from typing import List, Dict

from main import app
from pydantic import Product

# Cashier class to handle cart operations
class Cart:
    def __init__(self):
        self.cart_items = []

    def add_to_cart(self, product, quantity):
        self.cart_items.append({"product": product, "quantity": quantity})
        return {"message": f"Added {quantity} of {product['name']} to the cart."}

    def remove_from_cart(self, product_id):
        self.cart_items = [item for item in self.cart_items if item['product']['id'] != product_id]
        return {"message": "Product removed from cart."}

    def get_cart(self):
        return self.cart_items

    def calculate_total(self):
        total = 0
        for item in self.cart_items:
            total += item['product']['selling_price'] * item['quantity']
        return total


cart = Cart()

@app.get("/cart/add/")
async def add_to_cart(barcode: str, quantity: int):
    product = Product.get_product(barcode)  # Assuming get_product returns a product dict
    if product and product != {"message": "Product not found."}:
        return cart.add_to_cart(product, quantity)
    return {"error": "Product not found."}

@app.get("/cart/view/")
async def view_cart():
    return cart.get_cart()

@app.get("/cart/remove/")
async def remove_from_cart(barcode: str):
    # You need to implement removing by product ID or barcode
    return cart.remove_from_cart(barcode)

@app.get("/cart/total/")
async def calculate_total():
    return {"total_amount": cart.calculate_total()}
