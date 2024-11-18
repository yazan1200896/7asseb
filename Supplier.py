from mysql.connector import Error

class Supplier:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        print("self.db_connector = ", self.db_connector)

    def add_supplier(self, name, phone, address):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute(
                """
                INSERT INTO supplier (name, phone, address)
                VALUES (%s, %s, %s)
                """,
                (name, phone, address)
            )
            self.db_connector.commit()
            return {"message": "Supplier added successfully"}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to add supplier: {e}"}

    def get_supplier(self, supplier_id):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("SELECT * FROM supplier WHERE supplier_id = %s", (supplier_id,))
            supplier = cursor.fetchone()

            if supplier:
                return supplier
            else:
                return {"message": "Supplier not found."}
        except Error as e:
            return {"error": f"Failed to retrieve supplier: {e}"}

    def update_supplier(self, supplier_id, **kwargs):
        try:
            cursor = self.db_connector.get_cursor()
            update_query = "UPDATE supplier SET "
            update_values = []

            for key, value in kwargs.items():
                update_query += f"{key} = %s, "
                update_values.append(value)
            update_query = update_query.rstrip(", ") + " WHERE supplier_id = %s"
            update_values.append(supplier_id)

            cursor.execute(update_query, tuple(update_values))
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Supplier updated successfully"}
            else:
                return {"message": "Supplier not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to update supplier: {e}"}

    def delete_supplier(self, supplier_id):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute("DELETE FROM supplier WHERE supplier_id = %s", (supplier_id,))
            self.db_connector.commit()

            if cursor.rowcount > 0:
                return {"message": "Supplier deleted successfully"}
            else:
                return {"message": "Supplier not found."}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to delete supplier: {e}"}
