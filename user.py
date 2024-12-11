from mysql.connector import Error

class User:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def add_user(self, username, email, password, role, company_id):
        try:
            cursor = self.db_connector.get_cursor()
            query = """
                INSERT INTO users (username, email, password, role, company_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, password, role, company_id))
            self.db_connector.commit()
            return {"message": "User added successfully"}
        except Error as e:
            self.db_connector.rollback()
            print(f"Error adding user: {e}")  # Log error for debugging
            return {"detail": f"Error adding user: {e}"}

    def get_user(self, user_id):
        try:
            cursor = self.db_connector.get_cursor()
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user if user else {"message": "User not found"}
        except Error as e:
            print(f"Error retrieving user: {e}")  # Log error for debugging
            return {"detail": f"Error retrieving user: {e}"}

    def get_all_users(self):
        try:
            cursor = self.db_connector.get_cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            return users if users else {"message": "No users found"}
        except Error as e:
            print(f"Error retrieving users: {e}")  # Log error for debugging
            return {"detail": f"Error retrieving users: {e}"}

    def delete_user(self, user_id):
        try:
            cursor = self.db_connector.get_cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            self.db_connector.commit()
            return {"message": "User deleted successfully"} if cursor.rowcount > 0 else {"message": "User not found"}
        except Error as e:
            self.db_connector.rollback()
            print(f"Error deleting user: {e}")  # Log error for debugging
            return {"detail": f"Error deleting user: {e}"}
