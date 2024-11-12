from mysql.connector import Error
class Product:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def add_product(self, name, quantity, purchase_price, selling_price, images, barcode, date):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute(
                """
                INSERT INTO product (name, quantity, purchase_price, selling_price, images, barcode, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (name, quantity, purchase_price, selling_price, images, barcode, date)
            )
            self.db_connector.commit()
            return {"message": "Product added successfully"}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to add product: {e}"}

    def get_product(self, barcode):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("SELECT * FROM product WHERE barcode = %s", (barcode,))
            product = cursor.fetchone()

            if product:
                return product
            else:
                return {"message": "Product not found."}
        except Error as e:
            return {"error": f"Failed to retrieve product: {e}"}

    def update_product(self, barcode, **kwargs):
        try:
            cursor = self.db_connector.get_cursor()
            update_query = "UPDATE product SET "
            update_values = []

            for key, value in kwargs.items():
                update_query += f"{key} = %s, "
                update_values.append(value)
            update_query = update_query.rstrip(", ") + " WHERE barcode = %s"
            update_values.append(barcode)

            cursor.execute(update_query, tuple(update_values))
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Product updated successfully"}
            else:
                return {"message": "Product not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to update product: {e}"}

    def delete_product(self, barcode):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("DELETE FROM product WHERE barcode = %s", (barcode,))
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Product deleted successfully"}
            else:
                return {"message": "Product not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to delete product: {e}"}

    def get_all_products(self):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("SELECT * FROM product")
            products = cursor.fetchall()
            return products if products else {"message": "No products found."}
        except Error as e:
            return {"error": f"Failed to retrieve products: {e}"}

    def increment_quantity(self, barcode, amount):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("UPDATE product SET quantity = quantity + %s WHERE barcode = %s", (amount, barcode))
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Quantity incremented successfully"}
            else:
                return {"message": "Product not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to increment quantity: {e}"}

    def decrement_quantity(self, barcode, amount):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("SELECT quantity FROM product WHERE barcode = %s", (barcode,))
            product = cursor.fetchone()

            if product and product[0] >= amount:
                cursor.execute("UPDATE product SET quantity = quantity - %s WHERE barcode = %s", (amount, barcode))
                self.db_connector.commit()
                return {"message": "Quantity decremented successfully"}
            else:
                return {"message": "Not enough stock to decrement."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to decrement quantity: {e}"}