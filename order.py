from mysql.connector import Error
from datetime import datetime


class Order:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def create_order(self, supplier_id, barcodes, quantities, state="Pending"):
        try:
            cursor = self.db_connector.get_cursor()
            order_date = datetime.now()

            # Insert the order into the `order` table
            cursor.execute(
                """
                INSERT INTO `order` (supplier_id, order_date, state)
                VALUES (%s, %s, %s)
                """,
                (supplier_id, order_date, state)
            )
            order_id = cursor.lastrowid

            # Insert products into the `order_product` table
            for barcode, quantity in zip(barcodes, quantities):
                cursor.execute(
                    """
                    INSERT INTO order_product (order_id, barcode, quantity)
                    VALUES (%s, %s, %s)
                    """,
                    (order_id, barcode, quantity)
                )

            self.db_connector.commit()
            return {"message": "Order created successfully", "order_id": order_id}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to create order: {e}"}

    def get_order(self, order_id):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("SELECT * FROM `order` WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()

            if order:
                cursor.execute(
                    """
                    SELECT * FROM order_product WHERE order_id = %s
                    """,
                    (order_id,)
                )
                products = cursor.fetchall()
                return {"order": order, "products": products}
            else:
                return {"message": "Order not found."}
        except Error as e:
            return {"error": f"Failed to retrieve order: {e}"}

    def update_order_state(self, order_id, new_state):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute(
                """
                UPDATE `order` SET state = %s WHERE order_id = %s
                """,
                (new_state, order_id)
            )
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Order state updated successfully"}
            else:
                return {"message": "Order not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to update order state: {e}"}

    def delete_order(self, order_id):
        try:
            cursor = self.db_connector.get_cursor()

            # Delete associated products first
            cursor.execute("DELETE FROM order_product WHERE order_id = %s", (order_id,))

            # Then delete the order
            cursor.execute("DELETE FROM `order` WHERE order_id = %s", (order_id,))
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Order deleted successfully"}
            else:
                return {"message": "Order not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to delete order: {e}"}
